import os
import sys

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.src.app.src.shared.database.model_discovery import discover_models


discover_models()

if "pytest" in sys.modules:
    # connect to test database (in memory SQLite) when running tests
    _database_url = "sqlite:///:memory:"
    db_engine: Engine = create_engine(
        _database_url, echo=False, connect_args={"check_same_thread": False}
    )
else:
    # for production, connect to production database

    database_url_env = os.getenv("DATABASE_URL")
    if not database_url_env:
        raise ValueError("DATABASE_URL not set!")

    _database_url = "postgresql+pg5432://" + database_url_env
    db_engine: Engine = create_engine(_database_url, echo=True)

_LocalSessionMaker = sessionmaker(
    bind=db_engine, autoflush=False, autocommit=False
)


def open_session() -> Session:
    """
    Opens a new session. After usage, the session is automatically closed.
    This method should not be invoked directly, but should be used with
    FastAPI's dependency injection pattern.

    :return: A new session that is automatically closed after usage.
    """
    session = _LocalSessionMaker()
    try:
        yield session
    finally:
        session.close()
