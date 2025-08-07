"""
This script initializes the database by creating all standard tables and converting
marked tables into Hypertables using TimescaleDB.
It is designed to be run in all environments.
"""

import os

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from backend.src.app.shared import logging
from backend.src.app.src.seed_dev import seed_dev_data
from backend.src.app.src.seed_prod import seed_prod_data
from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.engine import db_engine
from backend.src.app.src.shared.database.model_discovery import discover_models

discover_models()

_environment = os.getenv("ENVIRONMENT")  # TEST / DEV / PROD

_logger = logging.get_logger(__name__)

_LocalSessionMaker = sessionmaker(
    bind=db_engine, autoflush=False, autocommit=False
)


# if __name__ == "__main__":
#    print("Dropping tables...")
#    BaseModel.metadata.drop_all(db_engine)
#    print("Done")
#    print("Creating tables...")
#    BaseModel.metadata.create_all(db_engine)
#    print("Done")


def is_prod_initialized() -> bool:
    """
    This function is used to check if the production database has already been
    initialized. If the environment is not PROD, raises an error.
    """
    if _environment != "PROD":
        raise EnvironmentError(
            f"PROD environment expected, but was '{_environment}'!"
        )
    return sqlalchemy.inspect(db_engine).has_table("Storage")


def generate_hypertables():
    with db_engine.connect() as connection:
        # Iterate through all models looking for the __timescaledb_hypertable__ marker
        for mapper in BaseModel.registry.mappers:
            model_class = mapper.class_
            if hasattr(model_class, "__timescaledb_hypertable__"):
                config = getattr(model_class, "__timescaledb_hypertable__")
                table_name = model_class.__tablename__
                time_column = config["time_column_name"]
                sql = text(
                    f"""
                        SELECT create_hypertable(
                            '"{table_name}"',
                            '{time_column}',
                            if_not_exists => TRUE
                        );
                    """
                )
                connection.execute(sql)
                _logger.info(
                    f"Hypertable '{table_name}' successfully created."
                )
        connection.commit()


def initialize_database():
    """
    Initializes the database:
    1. Creates all standard tables using BaseModel.metadata.create_all.
    2. Converts marked tables into Hypertables (only when not in test mode).
    """
    session = _LocalSessionMaker()
    if _environment == "PROD" and is_prod_initialized():
        _logger.info(
            "Production database already initialized. Skipping further initialization."
        )
        return

    # drop and re-create tables
    BaseModel.metadata.drop_all(db_engine)
    BaseModel.metadata.create_all(db_engine)
    _logger.info("Successfully recreated database.")

    # seed database if needed
    if _environment == "TEST":
        _logger.info(
            "Test mode detected, skipping seeding and Hypertable creation."
        )
        return
    elif _environment == "DEV":
        _logger.info(
            "Development mode detected. Creating hypertables and seeding development data..."
        )
        generate_hypertables()
        seed_dev_data(session)
    elif _environment == "PROD":
        _logger.info(
            "Production mode detected. Creating hypertables and seeding production data..."
        )
        generate_hypertables()
        seed_prod_data(session)
    else:
        msg = (
            "Unknown environment detected. Aborting database initialization. Have you set the ENVIRONMENT variable "
            "to either TEST, DEV or PROD?"
        )
        _logger.error(msg)
        raise EnvironmentError(msg)

    _logger.info("Database initialization complete.")
