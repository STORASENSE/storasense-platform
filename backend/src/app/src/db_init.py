"""
This script initializes the database by creating all standard tables and converting
marked tables into Hypertables using TimescaleDB. It is designed to be run in both
production and development environments, while skipping the Hypertable creation
when running tests against an in-memory SQLite database.
"""

import sys

from sqlalchemy import text

from backend.src.app.src.seed import seed_initial_data
from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.engine import db_engine, open_session
from backend.src.app.src.shared.database.model_discovery import discover_models


discover_models()


# if __name__ == "__main__":
#    print("Dropping tables...")
#    BaseModel.metadata.drop_all(db_engine)
#    print("Done")
#    print("Creating tables...")
#    BaseModel.metadata.create_all(db_engine)
#    print("Done")


def check_if_tables_exist() -> (
    bool
):  # TODO: check if the sensor with seeded id already exists
    """
    Checks if the database schema already exists.
    Returns True if the schema exists, False otherwise.
    This is used to avoid unnecessary re-initialization of the database.
    """
    # try:
    #     known_sensor_id = UUID("584ccf3a-0239-3b39-a07d-917a6417234a")
    #     statement = select(SensorModel).where(
    #         SensorModel.id == known_sensor_id
    #     )
    #     # result = db_engine.execute(statement).fetchone()
    #     # return result is not None
    #
    # except Exception as e:
    #     print(f"Error checking if tables exist: {e}")
    #     return False


def initialize_database():
    """
    Initializes the database:
    1. Creates all standard tables using BaseModel.metadata.create_all.
    2. Converts marked tables into Hypertables (only when not in test mode).
    """

    print("Checking if database initialization is needed...")
    if check_if_tables_exist():
        print("Database already initialized. Skipping further initialization.")
        return

    print("Database schema not found. Starting database initialization...")

    # Idempotent - check if tables already exist before creating them
    BaseModel.metadata.create_all(db_engine)
    print("Standard tables successfully checked/created.")

    # Seed initial data into the database
    print("Seeding initial data...")
    with open_session() as session:
        seed_initial_data(session)

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
