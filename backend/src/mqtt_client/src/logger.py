import logging
import logging.handlers
import os
import sys
import time
from typing import cast

import structlog
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.typing import BindableLogger


def configure_logging():
    """
    Central setup call, ideally at the very beginning of your application:
      from shared.logging import configure_logging
      configure_logging()
    """
    # 1) Configure standard logger
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level_value = getattr(logging, log_level, logging.INFO)

    # Get root logger and set level
    root_logger = get_logger()
    root_logger.setLevel(log_level_value)

    # Remove existing handlers
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    # INFO and WARNING -> stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    # Only allow levels below ERROR
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    stdout_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
    )
    root_logger.addHandler(stdout_handler)

    # ERROR and higher -> stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
    )
    root_logger.addHandler(stderr_handler)

    # Log rotation: Rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.getenv("LOG_FILE", "app.log"),
        maxBytes=int(os.getenv("LOG_MAX_BYTES", "10485760")),  # 10MB default
        backupCount=int(os.getenv("LOG_BACKUP_COUNT", "5")),
    )
    file_handler.setLevel(log_level_value)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
    )
    root_logger.addHandler(file_handler)

    # Uvicorn/FastAPI Integration: use the same handlers for uvicorn loggers
    for uv_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uv_logger = logging.getLogger(uv_name)
        uv_logger.handlers = root_logger.handlers
        uv_logger.setLevel(log_level_value)
        uv_logger.propagate = False

    # Optional monitoring: HTTP handler for ELK/Logstash
    logstash_url = os.getenv("LOGSTASH_URL")
    if logstash_url:
        http_handler = logging.handlers.HTTPHandler(
            host=logstash_url,
            url=os.getenv("LOGSTASH_ENDPOINT", "/"),
            method="POST",
        )
        http_handler.setLevel(logging.INFO)
        root_logger.addHandler(http_handler)

    # 2) Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),  # ISO timestamp
            structlog.processors.add_log_level,  # Level as field
            structlog.processors.StackInfoRenderer(),  # Stack info when needed
            structlog.processors.format_exc_info,  # exception info
            structlog.processors.JSONRenderer(),  # Output as JSON
        ],
        context_class=dict,
        # Bridge to stdlib logger
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=cast(type[BindableLogger], structlog.stdlib.BoundLogger),
        cache_logger_on_first_use=True,
    )


# Note: For FastAPI apps, the middleware should also be included
# from shared.logging import add_request_middleware


def get_logger(name=None):
    """
    Returns a structlog logger, tagged with the module name.
    Use in each module:
      from shared.logging import get_logger
      logger = get_logger(__name__)
    """
    return structlog.get_logger(name)


def add_request_middleware(app: FastAPI):
    logger = get_logger("request")

    class RequestLoggingMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(
                "http_request",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=f"{process_time:.4f}s",
            )
            return response

    app.add_middleware(RequestLoggingMiddleware)
