import logging
from zoneinfo import ZoneInfo
from datetime import datetime

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.token  = getattr(record, 'token',  '')
        record.role   = getattr(record, 'role',   '')
        record.path   = getattr(record, 'path',   '')
        record.method = getattr(record, 'method', '')
        return True

fmt = "%(asctime)s %(levelname)s token=%(token)s role=%(role)s path=%(path)s method=%(method)s %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S %Z"

formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
formatter.converter = lambda *args: datetime.now(ZoneInfo("Europe/Kyiv")).timetuple()

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("api")
logger.handlers = [handler]
logger.addFilter(ContextFilter())
