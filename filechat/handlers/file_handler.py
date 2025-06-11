# handlers/file_handler.py
from pathlib import Path
import mmap, os, tempfile, shutil
from filechat.constants import MAX_FILE_SIZE

SUPPORTED = {".txt", ".md"}

class FileHandler:
    """Load & save files on the local filesystem."""

    # ---------- LOAD ----------
    def load(self, path: str) -> str:
        """
        Read UTF-8 text from *path* if ≤ MAX_FILE_SIZE.
        Uses mmap for zero-copy speed on large files.

        Raises:
            FileNotFoundError – if path does not exist.
            ValueError – if file is > MAX_FILE_SIZE.
        """
        p = Path(path).expanduser().resolve()
        if p.suffix.lower() not in SUPPORTED:
            raise ValueError("415 Unsupported Media Type")
        if p.stat().st_size > MAX_FILE_SIZE:
            raise ValueError("File exceeds 10 MB limit")

        with p.open("r+b") as fh, mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as buf:
            return buf.read().decode("utf-8")

    # ---------- SAVE ----------
    def save(self, path: str, content: str):
        """
        Atomically write *content* to *path* and return absolute Path.
        """
        p = Path(path).expanduser().resolve()
        if p.suffix.lower() not in SUPPORTED:
            raise ValueError("415 Unsupported Media Type")

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            tmp.write(content)
            tmp.flush()
            os.fsync(tmp.fileno())
        shutil.move(tmp.name, p)          # atomic on POSIX
        return p