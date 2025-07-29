import os
import sys

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.src.app.src.shared.database.model_discovery import discover_models


discover_models()

if "pytest" in sys.modules:
    _database_url = "sqlite:///:memory:"
    db_engine: Engine = create_engine(
        _database_url, echo=False, connect_args={"check_same_thread": False}
    )
else:
    _database_url = "postgresql+pg5432://" + os.getenv("DATABASE_URL")
    db_engine: Engine = create_engine(_database_url, echo=True)

_LocalSessionMaker = sessionmaker(
    bind=db_engine, autoflush=False, autocommit=False
)


def open_session() -> Session:
    session = _LocalSessionMaker()
    try:
        yield session
    finally:
        session.close()
