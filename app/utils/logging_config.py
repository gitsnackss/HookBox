"""Configure structured JSON logging."""
import logging
import json
from pythonjsonlogger import jsonlogger
from app.config import settings

def configure_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(settings.log_level.upper())
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s %(project_id)s"
    )
    log_handler.setFormatter(formatter)
    logger.handlers = [log_handler]
