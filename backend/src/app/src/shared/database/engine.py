import os
import sys

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv

from backend.src.app.src.shared.database.model_discovery import discover_models

discover_models()


load_dotenv(override=True)

# connect to test database (in memory SQLite) when running tests

if "pytest" in sys.modules:
    _database_url = "sqlite:///:memory:"
    db_engine: Engine = create_engine(
        _database_url, echo=False, connect_args={"check_same_thread": False}
    )

# for production, connect to production database

else:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")

    _database_url_env = f"{user}:{password}@{host}:{port}/{db_name}"
    if not _database_url_env:
        raise ValueError("DATABASE-envs not set!")

    _database_url = "postgresql+pg8000://" + _database_url_env
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
