import logging
import sys
from logging import Logger, StreamHandler

from asgi_correlation_id import CorrelationIdFilter
from pythonjsonlogger.json import JsonFormatter
from uvicorn.logging import DefaultFormatter

from app.core import config

discarded_keys = ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
            'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
            'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
            'thread', 'threadName', 'processName', 'process', 'message',
            'taskName', 'asctime']

class ExFormatter(DefaultFormatter):
    def format(self, record):
        string = super().format(record)
        extra = {k: v for k,v in record.__dict__.items()
             if k not in discarded_keys}
        if len(extra)>0:
            string += " - extra: " + str(extra)
        return string

class TextFormatter(logging.Formatter):
    def format(self,record):
        extra = []

        for key,value in record.__dict__.items():
            if key not in discarded_keys:
                extra.append(f"{key}: \"{value}\"")

        timestamp = self.formatTime(record, self.datefmt)


        return f"{timestamp} | {record.levelname} | {record.getMessage()} | {' '.join(extra)}"
        

def setup_logger():
    if not config.settings.LOG_ENABLED:
        return

    logger = logging.getLogger(config.settings.app_name)

    logger.setLevel(logging.INFO)

    if config.settings.LOG_LEVEL == config.LogLevels.Debug:
        logger.setLevel(logging.DEBUG)

    logger.addFilter(
        CorrelationIdFilter(
            uuid_length=32 if not config.settings.development else 6,
            default_value="-",
        )
    )

    handler = StreamHandler(sys.stdout)
    if config.settings.LOG_STRUCTURED:
        handler.setFormatter(JsonFormatter(json_ensure_ascii=False))
    else:
        handler.setFormatter(TextFormatter(datefmt="%Y-%m-%d %H:%M:%S"))

    logger.addHandler(handler)

def get_logger() -> Logger:
    logger = logging.getLogger(config.settings.app_name)

    return logger
