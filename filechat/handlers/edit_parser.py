# handlers/edit_parser.py
import re
from dataclasses import dataclass

@dataclass
class EditOp:
    verb: str
    selector: str
    payload: str | None = None

EDIT_RE = re.compile(r"^/(replace|append|delete)\s+(.+?)(?:\s+<<\s*(.*?)\s*>>)?$", re.S)

def parse_edit(command: str) -> EditOp:
    """
    Converts `/replace foo <<bar>>` → EditOp(verb='replace', selector='foo', payload='bar')
    """
    m = EDIT_RE.match(command.strip())
    if not m:
        raise ValueError("Malformed edit command")
    verb, sel, body = m.groups()
    return EditOp(verb, sel, body)
