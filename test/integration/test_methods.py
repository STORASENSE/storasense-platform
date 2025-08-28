from test.rest_functionality.rest_methods import (
    get_request,
    post_request,
)
import psycopg2
import os


def create_storage():
    post_request("storages", {"name": os.getenv("TEST_STORAGE_NAME")})
    return next(
        storage["id"]
        for storage in get_request("storages/myStorages")
        if storage["name"] == os.getenv("TEST_STORAGE_NAME")
    )


def create_sensor(storage_id):
    post_request(
        f"sensors/{os.getenv('TEST_SENSOR_ID')}",
        {
            "storage_id": storage_id,
            "type": "TEMPERATURE_INSIDE",
            "name": "test_sensor",
            "allowed_min": 0,
            "allowed_max": 100,
        },
    )
    return os.getenv("TEST_SENSOR_ID")


def get_database_connection():
    """
    Establishes and returns a connection to the PostgreSQL database using environment variables.
    """
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
