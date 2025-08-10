# shared/logging.py
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
    Zentraler Setup-Aufruf, idealerweise ganz am Anfang deiner Anwendung:
      from shared.logging import configure_logging
      configure_logging()
    """
    # 1) Standard-Logger konfigurieren
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level_value = getattr(logging, log_level, logging.INFO)

    # Wurzel-Logger holen und Level setzen
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level_value)

    # Vorhandene Handler entfernen
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    # INFO und WARNING -> stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    # Nur Levels unter ERROR durchlassen
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    stdout_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
    )
    root_logger.addHandler(stdout_handler)

    # ERROR und höher -> stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
    )
    root_logger.addHandler(stderr_handler)

    # Log-Rotation: Rotating file handler
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

    # Optional Monitoring: HTTP handler für ELK/Logstash
    logstash_url = os.getenv("LOGSTASH_URL")
    if logstash_url:
        http_handler = logging.handlers.HTTPHandler(
            host=logstash_url,
            url=os.getenv("LOGSTASH_ENDPOINT", "/"),
            method="POST",
        )
        http_handler.setLevel(logging.INFO)
        root_logger.addHandler(http_handler)

    # 2) Structlog konfigurieren
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),  # ISO-Zeitstempel
            structlog.processors.add_log_level,  # Level als Feld
            structlog.processors.StackInfoRenderer(),  # Stack-Infos bei Bedarf
            structlog.processors.format_exc_info,  # exception info
            structlog.processors.JSONRenderer(),  # Ausgabe als JSON
        ],
        context_class=dict,
        # Brücke zum stdlib-Logger
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=cast(type[BindableLogger], structlog.stdlib.BoundLogger),
        cache_logger_on_first_use=True,
    )


# Hinweis: Für FastAPI-Apps sollte zusätzlich die Middleware eingebunden werden
# from shared.logging import add_request_middleware


def get_logger(name=None):
    """
    Liefert einen Structlog-Logger, getagged mit dem Modul-Namen.
    Verwende in jedem Modul:
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
