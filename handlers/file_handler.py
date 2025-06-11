# handlers/file_handler.py
from pathlib import Path
from filechat.constants import MAX_FILE_SIZE
import mmap

class FileHandler:
    """Load & save files on the local filesystem."""

    def load(self, path: str) -> str:
        """
        Read UTF-8 text from *path* if ≤ MAX_FILE_SIZE.
        Uses mmap for zero-copy speed on large files.

        Raises:
            FileNotFoundError – if path does not exist.
            ValueError – if file is > MAX_FILE_SIZE.
        """
        p = Path(path).expanduser().resolve()
        if p.stat().st_size > MAX_FILE_SIZE:
            raise ValueError("File exceeds 10 MB limit")

        with p.open("r+b") as fh, mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as buf:
            return buf.read().decode("utf-8")
