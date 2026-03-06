from typing import List, Dict, Any
import numpy as np
from mcp.types import TextContent

def format_search_results(results: List[Dict[str, Any]]) -> List[TextContent]:
    """Format LanceDB search results into MCP TextContent objects."""
    formatted_results = []
    for res in results:
        # res contains fields like 'text' (or 'content'), 'path' (or 'source'), 'chunk_id', and '_distance'
        content = res.get("text") or res.get("content") or "No content"
        source = res.get("path") or res.get("source") or "Unknown source"
        # We don't have a timestamp field in the current index schema, but we'll check just in case
        timestamp = res.get("timestamp")
        distance = res.get("_distance", 1.0)
        
        # Calculate a similarity score from distance (L2 distance: 0 is perfect match)
        # Score = 1 / (1 + distance) is a common way to map [0, inf) to [1, 0]
        similarity = 1.0 / (1.0 + distance)
        
        text_lines = [
            f"Source: {source}",
            f"Similarity: {similarity:.2%}"
        ]
        if timestamp:
            text_lines.insert(1, f"Timestamp: {timestamp}")
            
        text_lines.append(f"\n{content}")
        
        formatted_text = "\n".join(text_lines)
        formatted_results.append(TextContent(type="text", text=formatted_text))
    
    return formatted_results

async def search_engram_tool(engram_server, query: str, limit: int = 10) -> List[TextContent]:
    """Execute semantic search and return formatted results."""
    if not engram_server.table or not engram_server.model:
        raise RuntimeError("Engram server not properly initialized (missing table or model)")
    
    # 1. Embed the query (Constitution: Local-First)
    query_vector = engram_server.model.encode(query)
    if isinstance(query_vector, np.ndarray):
        query_vector = query_vector.tolist()
    
    # 2. Search LanceDB
    results = engram_server.table.search(query_vector).limit(limit).to_list()
    
    # 3. Format and return
    if not results:
        return [TextContent(type="text", text="No relevant memories found.")]
        
    return format_search_results(results)
