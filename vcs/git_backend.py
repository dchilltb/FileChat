from pygit2 import Repository, Signature
from pathlib import Path
from datetime import datetime

def commit(path: Path, message: str):
    repo = Repository(f"{path.parent}/.git")
    index = repo.index
    index.add(str(path.relative_to(repo.workdir)))
    index.write()
    author = Signature("FileChat Bot", "bot@filechat.ai")
    oid = repo.create_commit(
        "HEAD",
        author,
        author,
        message,
        index.write_tree(),
        [repo.head.target] if repo.head_is_unborn is False else [],
    )
    return str(oid)