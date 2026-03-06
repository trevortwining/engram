import os
import sys
import logging
import asyncio
import signal
from typing import Optional, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolRequest
import lancedb
from sentence_transformers import SentenceTransformer

from engram.mcp.tools import search_engram_tool

# Configure logging to stderr as required for MCP stdio transport
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("engram-mcp")

class EngramServer:
    def __init__(self, db_path: str = "engram.lancedb"):
        self.server = Server("engram")
        self.db_path = db_path
        self.db: Optional[lancedb.DBConnection] = None
        self.table: Optional[lancedb.table.Table] = None
        self.model: Optional[SentenceTransformer] = None
        
        self.setup_handlers()

    def setup_handlers(self):
        """Setup MCP handlers for tool listing and execution."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="search_engram",
                    description="Search the user's engram memory store using semantic similarity.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The natural language query to search for."
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return.",
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> List[TextContent]:
            if name == "search_engram":
                try:
                    query = arguments.get("query")
                    limit = arguments.get("limit", 10)
                    if not query:
                        return [TextContent(type="text", text="Error: Query is required for search_engram")]
                    
                    if not self.table or not self.model:
                        return [TextContent(type="text", text="Error: Server not initialized correctly (database or model missing).")]
                    
                    return await search_engram_tool(self, query, limit)
                except Exception as e:
                    logger.error(f"Error executing search: {e}")
                    return [TextContent(type="text", text=f"Error executing search: {str(e)}")]
            
            raise ValueError(f"Unknown tool: {name}")

    async def initialize(self):
        """Initialize database and embedding model."""
        try:
            logger.info(f"Initializing Engram MCP server with DB at {self.db_path}")
            
            # Initialize model (Constitution: Local-First, Always)
            logger.info("Loading embedding model...")
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise RuntimeError(f"Embedding model loading failed: {str(e)}")
            
            # Initialize database
            if not os.path.exists(self.db_path):
                logger.error(f"Database path {self.db_path} does not exist.")
                raise FileNotFoundError(f"Database not found at {self.db_path}. Please run 'engram index <path>' first.")

            # T014: Handle database lock or connection issues with a simple retry
            for attempt in range(3):
                try:
                    self.db = lancedb.connect(self.db_path)
                    self.table = self.db.open_table("memories")
                    break
                except Exception as e:
                    if "lock" in str(e).lower() and attempt < 2:
                        logger.warning(f"Database locked, retrying in 1s (attempt {attempt+1}/3)...")
                        await asyncio.sleep(1)
                    else:
                        logger.error(f"Database connection failed: {e}")
                        raise RuntimeError(f"Database connection failed: {str(e)}")

            logger.info("Database and model initialized successfully.")
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            raise

    def get_server(self) -> Server:
        return self.server

async def main(db_path: str = "engram.lancedb"):
    engram_server = EngramServer(db_path=db_path)
    try:
        await engram_server.initialize()
    except Exception as e:
        # In stdio mode, we must exit if we can't initialize
        logger.critical(f"Server could not start: {e}")
        sys.exit(1)

    # Graceful shutdown handlers
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def shutdown():
        logger.info("Shutting down Engram MCP server...")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown)

    async with stdio_server() as (read_stream, write_stream):
        server_task = asyncio.create_task(
            engram_server.get_server().run(
                read_stream,
                write_stream,
                engram_server.get_server().create_initialization_options()
            )
        )
        
        # Wait for either server completion or stop signal
        done, pending = await asyncio.wait(
            [server_task, stop_event.wait()],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        if not server_task.done():
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

if __name__ == "__main__":
    asyncio.run(main())
