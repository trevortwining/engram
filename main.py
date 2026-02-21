import typer
import lancedb
import pyarrow as pa
from sentence_transformers import SentenceTransformer
from pathlib import Path
import os
import json

app = typer.Typer()

# Constants
DB_PATH = Path("engram.lancedb")
MODEL_NAME = "all-MiniLM-L6-v2"

@app.command()
def index(path: str):
    """Index a directory of Markdown files."""
    typer.echo(f"Indexing directory: {path}")
    
    # 1. Initialize DB and Model
    db = lancedb.connect(DB_PATH)
    model = SentenceTransformer(MODEL_NAME)
    
    # 2. Collect Markdown Files
    md_files = list(Path(path).rglob("*.md"))
    typer.echo(f"Found {len(md_files)} Markdown files.")
    
    data = []
    for file in md_files:
        content = file.read_text(encoding="utf-8")
        # Simple chunking by paragraph for now
        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
        
        for i, chunk in enumerate(chunks):
            # We'll use the model to encode the chunk
            embedding = model.encode(chunk).tolist()
            data.append({
                "vector": embedding,
                "text": chunk,
                "path": str(file),
                "chunk_id": i
            })
            
    # 3. Write to LanceDB
    if data:
        table = db.create_table("memories", data=data, mode="overwrite")
        typer.echo(f"Successfully indexed {len(data)} chunks into 'memories' table.")
    else:
        typer.echo("No content found to index.")

@app.command()
def search(query: str, limit: int = 5):
    """Search the memory for a given query."""
    if not DB_PATH.exists():
        typer.echo("Database not found. Please run 'index' first.")
        return

    db = lancedb.connect(DB_PATH)
    table = db.open_table("memories")
    model = SentenceTransformer(MODEL_NAME)
    
    query_vector = model.encode(query).tolist()
    
    # Use LanceDB vector search
    results = table.search(query_vector).limit(limit).to_list()
    
    # Format for Agent Ingestion
    output = []
    for r in results:
        output.append({
            "text": r["text"],
            "path": r["path"],
            "score": float(r["_distance"]) # Distance score
        })
        
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    app()
