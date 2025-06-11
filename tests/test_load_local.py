# tests/test_load_local.py
from pathlib import Path
from handlers.file_handler import FileHandler

def test_load_small_file(tmp_path: Path):
    data = "A" * (5 * 1024 * 1024)  # 5 MB
    f = tmp_path / "demo.txt"
    f.write_text(data)
    assert FileHandler().load(str(f)) == data
