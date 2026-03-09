import logging
import sys
from morphosx.app.settings import settings


def setup_logging():
    """
    Configure structured-ready logging for MorphosX.
    """
    logger = logging.getLogger("morphosx")
    level = logging.DEBUG if settings.debug else logging.INFO
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Global logger instance
logger = setup_logging()
