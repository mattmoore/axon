import logging
from logging import Formatter, LogRecord
import json

class JsonFormatter(Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()

    def format(self, record: LogRecord) -> str:
        record_dict = {
            "level": record.levelname,
            "date": self.formatTime(record),
            "message": record.getMessage(),
            "module": record.module,
            "lineno": record.lineno,
        }
        return json.dumps(record_dict)

def make_logger(name):
    logger = logging.getLogger(name)
    logging_handler = logging.StreamHandler()
    logging_handler.setFormatter(JsonFormatter())
    logger.handlers = [logging_handler]
    logger.setLevel(logging.DEBUG)
    return logger
