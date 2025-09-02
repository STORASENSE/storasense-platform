import os
import json
import psycopg2
from confluent_kafka import Producer


def push_all_sensors_to_kafka():
    """
    Push all sensors with their allowed min/max values and admin email to Kafka topic "sensor_values".
    THis function is only called once at application startup to initialize the Kafka topic with sensor data - e.g. after system restart.
    """
    # DB connection
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    cur = conn.cursor()

    # Kafka Producer init
    KAFKA_HOST = os.getenv("KAFKA_HOST")
    if not KAFKA_HOST:
        raise EnvironmentError("KAFKA_HOST environment variable not set")
    producer = Producer(
        {"bootstrap.servers": KAFKA_HOST, "partitioner": "murmur2"}
    )

    # Sensoren query
    cur.execute(
        'SELECT id, allowed_min, allowed_max, storage_id FROM "Sensor"'
    )
    sensors = cur.fetchall()

    for sensor in sensors:
        sensor_id, allowed_min, allowed_max, storage_id = sensor

        # Admin-User for storage
        cur.execute(
            """
            SELECT u.email
            FROM "UserStorageAccess" usa
            JOIN "User" u ON usa.user_id = u.id
            WHERE usa.storage_id = %s AND usa.role = 'ADMIN'
            LIMIT 1
        """,
            (storage_id,),
        )
        admin = cur.fetchone()
        email = admin[0] if admin else None

        sensor_data = {
            "sensorId": str(sensor_id),
            "allowedMin": allowed_min,
            "allowedMax": allowed_max,
            "email": email,
        }
        producer.produce(
            "sensor_values",
            key=str(sensor_id).encode("utf-8"),
            value=json.dumps(sensor_data).encode("utf-8"),
        )

    producer.flush()
    cur.close()
    conn.close()


if __name__ == "__main__":
    push_all_sensors_to_kafka()
