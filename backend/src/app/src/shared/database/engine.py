import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

_database_url = os.getenv("DATABASE_URL")

db_engine: Engine = create_engine(
    f"postgresql+pg8000://{_database_url}", echo=True
)
_LocalSessionMaker = sessionmaker(
    bind=db_engine, autoflush=False, autocommit=False
)


def open_session() -> Session:
    session = _LocalSessionMaker()
    try:
        yield session
    finally:
        session.close()
