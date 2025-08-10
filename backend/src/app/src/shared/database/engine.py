import os
import sys
import time
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv

from backend.src.app.src.shared.database.model_discovery import discover_models
from backend.src.app.src.shared.logging import get_logger

logger = get_logger(__name__)

discover_models()
load_dotenv(override=True)

# connect to test database (in memory SQLite) when running tests
if "pytest" in sys.modules:
    _database_url = "sqlite:///:memory:"
    db_engine: Engine = create_engine(
        _database_url, echo=False, connect_args={"check_same_thread": False}
    )

# connect to postgres database when being run in production / dev
else:
    max_retries = 3
    retry_delay = 1  # Initial delay in seconds

    for attempt in range(1, max_retries + 1):
        try:
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            host = os.getenv("POSTGRES_HOST")
            port = os.getenv("POSTGRES_PORT")
            db_name = os.getenv("POSTGRES_DB")

            if not all([user, password, host, port, db_name]):
                missing = [
                    var
                    for var, val in {
                        "POSTGRES_USER": user,
                        "POSTGRES_PASSWORD": password,
                        "POSTGRES_HOST": host,
                        "POSTGRES_PORT": port,
                        "POSTGRES_DB": db_name,
                    }.items()
                    if not val
                ]
                raise ValueError(
                    f"Missing environment variables: {', '.join(missing)}"
                )

            _database_url_env = f"{user}:{password}@{host}:{port}/{db_name}"
            _database_url = "postgresql+pg8000://" + _database_url_env
            db_engine: Engine = create_engine(_database_url, echo=True)

            # Test connection to ensure database is reachable
            with db_engine.connect() as connection:
                pass

            logger.info("Database connection successfully established.")
            break  # Connection successful, exit loop

        except (SQLAlchemyError, ValueError) as e:
            if attempt < max_retries:
                wait_time = retry_delay * (
                    2 ** (attempt - 1)
                )  # Exponential backoff
                logger.warning(f"Connection attempt {attempt} failed: {e}")
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(
                    f"All connection attempts failed. Last error: {e}",
                    file=sys.stderr,
                )
                sys.exit(1)  # Exit program when all attempts fail

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
