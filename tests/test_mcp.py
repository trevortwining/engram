import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from engram.mcp.server import EngramServer
from engram.mcp.tools import search_engram_tool

@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.open_table.return_value = mock_table
    return mock_db, mock_table

@pytest.fixture
def mock_model():
    mock_model = MagicMock()
    # mock encode for embedding queries
    mock_model.encode.return_value = [0.1] * 384
    return mock_model

@pytest.mark.asyncio
async def test_server_initialization(mock_db, mock_model, monkeypatch):
    """Test that server initializes correctly when DB exists."""
    # Mock lancedb.connect and SentenceTransformer
    monkeypatch.setattr("lancedb.connect", lambda path: mock_db[0])
    monkeypatch.setattr("os.path.exists", lambda path: True)
    monkeypatch.setattr("engram.mcp.server.SentenceTransformer", lambda name: mock_model)
    
    server = EngramServer(db_path="mock.lancedb")
    await server.initialize()
    
    assert server.db is not None
    assert server.table is not None
    assert server.model is not None
    mock_db[0].open_table.assert_called_once_with("memories")

@pytest.mark.asyncio
async def test_server_initialization_fail(mock_model, monkeypatch):
    """Test server initialization failure when DB is missing."""
    monkeypatch.setattr("os.path.exists", lambda path: False)
    monkeypatch.setattr("engram.mcp.server.SentenceTransformer", lambda name: mock_model)
    
    server = EngramServer(db_path="nonexistent.lancedb")
    with pytest.raises(FileNotFoundError):
        await server.initialize()

@pytest.mark.asyncio
async def test_server_stability_soak(mock_db, mock_model, monkeypatch):
    """SC-004: Test server stability over 100 sequential search queries."""
    monkeypatch.setattr("lancedb.connect", lambda path: mock_db[0])
    monkeypatch.setattr("os.path.exists", lambda path: True)
    monkeypatch.setattr("engram.mcp.server.SentenceTransformer", lambda name: mock_model)
    
    # Mock table search results
    mock_table = mock_db[1]
    mock_table.search.return_value.limit.return_value.to_list.return_value = [
        {"text": "test content", "path": "test.md", "_distance": 0.1}
    ]
    
    server = EngramServer(db_path="mock.lancedb")
    await server.initialize()
    
    for i in range(100):
        results = await search_engram_tool(server, f"query {i}", limit=5)
        assert len(results) == 1
        assert "Similarity" in results[0].text
    
    assert i == 99
