import structlog
from filechat.constants import LOG_SCHEMA_VERSION

from telemetry.collector import record_event
record_event("file_saved", path=str(p), bytes=len(content))

structlog.configure(processors=[structlog.processors.JSONRenderer()])

log = structlog.get_logger(schema=LOG_SCHEMA_VERSION)

def record_event(event: str, **kw):
    log.info(event, **kw)

