# shared/logging.py
import logging
import os
import sys
from typing import cast

import structlog
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
    stdout_handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.addHandler(stdout_handler)

    # ERROR und höher -> stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.addHandler(stderr_handler)

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


def get_logger(name=None):
    """
    Liefert einen Structlog-Logger, getagged mit dem Modul-Namen.
    Verwende in jedem Modul:
      from shared.logging import get_logger
      logger = get_logger(__name__)
    """
    return structlog.get_logger(name)
