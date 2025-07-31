import os

import requests
from database import get_db_connection


def send_one_value():
    connection = get_db_connection()
    with connection:
        row = connection.execute(
            # "select message_id, timestamp,sensor_id,"
            # + "value from sensor_data limit 1"
        ).fetchone()
        if row:
            row_id = row[0]
            timestamp = row[1]
            sensor_id = row[2]
            value = row[3]
            response = requests.post(
                os.getenv("MQTT_BACKEND_URL"),
                json={
                    "id": row_id,
                    "timestamp": timestamp,
                    "sensor_id": sensor_id,
                    "value": value,
                },
            )
            if response.status_code == int(os.getenv("MQTT_HTTP_RESPONSE_OK")):
                connection.execute(
                    #         "DELETE FROM sensor_data WHERE id = ?", (row_id,)
                )


def start_rest_client(stop_event):
    while not stop_event.is_set():
        send_one_value()
