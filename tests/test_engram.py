import json
from importlib import util
from pathlib import Path

import lancedb
import pytest

ENGRAM_MAIN_PATH = Path(__file__).resolve().parents[1] / "main.py"
spec = util.spec_from_file_location("engram_main", ENGRAM_MAIN_PATH)
engram_main = util.module_from_spec(spec)
spec.loader.exec_module(engram_main)


class DummyArray(list):
    def tolist(self):
        return list(self)


class DummyModel:
    def __init__(self, *args, **kwargs):
        pass

    def encode(self, payload):
        if isinstance(payload, list):
            return [DummyArray([float(len(item))] * 4) for item in payload]
        return DummyArray([float(len(payload))] * 4)


def _prepare_env(tmp_path, monkeypatch):
    db_path = tmp_path / "engram.lancedb"
    monkeypatch.setattr(engram_main, "DB_PATH", db_path)
    monkeypatch.setattr(engram_main, "SentenceTransformer", DummyModel)
    return db_path


def _create_sample_docs(dir_path: Path):
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / "notes.md"
    file_path.write_text(
        """Paragraph one.

Paragraph two has more detail.

Paragraph three is the final chunk."""
    )
    return file_path


def test_index_creates_chunks(tmp_path, monkeypatch):
    _prepare_env(tmp_path, monkeypatch)
    docs_dir = tmp_path / "vault"
    _create_sample_docs(docs_dir)

    engram_main.index(str(docs_dir))

    db = lancedb.connect(engram_main.DB_PATH)
    table = db.open_table("memories")
    rows = table.to_arrow().to_pylist()

    assert len(rows) == 3
    assert all("text" in row for row in rows)
    assert all("path" in row for row in rows)


def test_search_outputs_json(tmp_path, monkeypatch, capsys):
    _prepare_env(tmp_path, monkeypatch)
    docs_dir = tmp_path / "vault"
    _create_sample_docs(docs_dir)

    engram_main.index(str(docs_dir))
    capsys.readouterr()
    engram_main.search("Paragraph", limit=2)

    output = capsys.readouterr().out.strip()
    assert output
    data = json.loads(output)

    assert isinstance(data, list)
    assert len(data) == 2
    for entry in data:
        assert {"text", "path", "score"}.issubset(entry)
        assert isinstance(entry["score"], float)
