"""
This script drops all tables from the connected database (if they exist)
and then creates all tables.

Note that this script is for development only, and future usage should
occur via a proper database migration tool, such as Alembic.
"""

import sys
from sqlalchemy import text

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.engine import db_engine
from backend.src.app.src.shared.database.model_discovery import discover_models


discover_models()


# if __name__ == "__main__":
#    print("Dropping tables...")
#    BaseModel.metadata.drop_all(db_engine)
#    print("Done")
#    print("Creating tables...")
#    BaseModel.metadata.create_all(db_engine)
#    print("Done")


def initialize_database():
    """
    Initializes the database:
    1. Creates all standard tables using BaseModel.metadata.create_all.
    2. Converts marked tables into Hypertables (only when not in test mode).
    """
    print("Starting database initialization...")

    BaseModel.metadata.create_all(db_engine)
    print("Standard tables successfully checked/created.")

    # IMPORTANT: We do not execute the TimescaleDB logic when testing against the in-memory SQLite database.
    if "pytest" in sys.modules:
        print("Test mode detected, skipping Hypertable creation.")
        print("Database initialization complete.")
        return

    # Create Hypertables for all models that have the __timescaledb_hypertable__ marker
    print("Production/Development mode: Creating Hypertables...")
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
                print(
                    f"Hypertable '{table_name}' successfully checked/created."
                )

        connection.commit()

    print("Database initialization complete.")
