import os
import sqlite3


def get_db_connection():
    return sqlite3.connect(os.getenv("MQTT_DATABASE_NAME", "mqtt_data.db"))


def init_db():
    connection = get_db_connection()
    with connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id INTEGER NOT NULL,
                timestamp INTEGER NOT NULL,
                value decimal(10, 2) NOT NULL);
            """
        )
    connection.close()
