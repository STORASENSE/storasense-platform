from test.integration.test_methods import get_database_connection
import os
from logging import getLogger


def cleanup_database():
    """
    Cleans up the test database by deleting all entries used during tests.
    """
    logger = getLogger(__name__)
    sensor_id = os.getenv("TEST_SENSOR_ID")
    storage_name = os.getenv("TEST_STORAGE_NAME")
    conn = get_database_connection()
    logger.info("Cleaning up the test database")
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'DELETE FROM "Measurements" WHERE sensor_id = %s', (sensor_id,)
            )
            cursor.execute('DELETE FROM "Sensor" WHERE id = %s', (sensor_id,))
            cursor.execute(
                'DELETE FROM "UserStorageAccess" WHERE storage_id = (SELECT id FROM "Storage" WHERE name = %s)',
                (storage_name,),
            )
            cursor.execute(
                'DELETE FROM "Storage" WHERE name = %s', (storage_name,)
            )
        conn.commit()
    except Exception as e:
        logger.error("Error cleaning up the test database : %s", e)
    logger.info("Cleanup completed")


if __name__ == "__main__":
    cleanup_database()
