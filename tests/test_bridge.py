import subprocess
import json
import os
import tempfile
import pytest
from pathlib import Path

# Path to the script we are testing
SCRIPT_PATH = Path(__file__).parent.parent / "engram-bridge" / "query.sh"

@pytest.fixture
def env_setup(tmp_path):
    """Sets up a temporary environment for testing."""
    # Create a dummy store directory
    store_dir = tmp_path / "dummy_store.lancedb"
    store_dir.mkdir()
    
    # Create a mock main.py that just returns empty json
    main_py = tmp_path / "main.py"
    main_py.write_text('print("[]")')

    env = os.environ.copy()
    env["ENGRAM_STORE"] = str(store_dir)
    # We need to mock 'uv run main.py' to not fail. 
    # Since the script hardcodes `uv run main.py search`, it's tricky to mock without altering the script.
    # The script uses 2>/dev/null, so it will just get empty output if uv fails, which is fine for our tests.
    # The output JSON will have "results": []
    
    yield env, tmp_path

def test_missing_store_env():
    """Test 1a: Missing ENGRAM_STORE fails fast."""
    env = os.environ.copy()
    if "ENGRAM_STORE" in env:
        del env["ENGRAM_STORE"]
    
    result = subprocess.run([str(SCRIPT_PATH), "test query"], env=env, capture_output=True, text=True)
    
    assert result.returncode == 1
    output = json.loads(result.stdout)
    assert "error" in output
    assert "ENGRAM_STORE environment variable is not set" in output["error"]

def test_invalid_store_path():
    """Test 1b: Invalid ENGRAM_STORE fails fast."""
    env = os.environ.copy()
    env["ENGRAM_STORE"] = "/path/that/does/not/exist/12345"
    
    result = subprocess.run([str(SCRIPT_PATH), "test query"], env=env, capture_output=True, text=True)
    
    assert result.returncode == 1
    output = json.loads(result.stdout)
    assert "error" in output
    assert "does not exist or is unreachable" in output["error"]

def test_query_composer(env_setup):
    """Test 2: Query Composer strips filler words."""
    env, _ = env_setup
    
    # "what did i decide about LanceDB" should become "LanceDB"
    result = subprocess.run([str(SCRIPT_PATH), "what did i decide about LanceDB"], env=env, capture_output=True, text=True)
    
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["query"] == "LanceDB"

    # "the quick brown fox" should strip "the"
    result = subprocess.run([str(SCRIPT_PATH), "the quick brown fox"], env=env, capture_output=True, text=True)
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["query"] == "quick brown fox"

def test_search_execution_structure(env_setup):
    """Test 3: Returns expected JSON structure."""
    env, _ = env_setup
    
    result = subprocess.run([str(SCRIPT_PATH), "test"], env=env, capture_output=True, text=True)
    
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert "status" in output
    assert "query" in output
    assert "results" in output

def test_reindex_control_stale(env_setup):
    """Test 4: Detects new files and marks as stale."""
    env, tmp_path = env_setup
    
    # Touch a new markdown file in the script's directory (or where it runs)
    # The script currently runs `find .` from MAIN_DIR which is the parent of engram-bridge.
    # To reliably test this without polluting the real dir, we have to simulate the condition.
    # Since the script does `cd "$MAIN_DIR"`, it checks the actual project repo.
    # We will create a temporary .md file in the actual repo for a split second to test this.
    
    test_md = SCRIPT_PATH.parent.parent / "temp_test_stale.md"
    test_md.touch()
    
    try:
        result = subprocess.run([str(SCRIPT_PATH), "test"], env=env, capture_output=True, text=True)
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["status"] == "stale"
        assert "Content changed" in output["message"]
    finally:
        test_md.unlink(missing_ok=True)
