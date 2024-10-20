import logging
from loguru import logger
from types import FrameType
from typing import cast

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# Configure loguru
logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

# Redirect standard logging to loguru
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)