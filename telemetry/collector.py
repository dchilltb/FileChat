"""
Lightweight wrapper around structlog that emits JSON-line events.
"""

import structlog
from filechat.constants import LOG_SCHEMA_VERSION

# Configure structlog once for the entire app
structlog.configure(processors=[structlog.processors.JSONRenderer()])

_log = structlog.get_logger(schema=LOG_SCHEMA_VERSION)

def record_event(event: str, **kwargs):
    """Log *event* plus arbitrary key/value metadata as a JSON object."""
    _log.info(event, **kwargs)