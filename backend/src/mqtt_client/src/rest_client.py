import math
import os
from datetime import datetime

import requests
from database import get_db_connection
from backend.src.shared.logging import logging

_logger = logging.getLogger(__name__)


def send_one_value():
    connection = get_db_connection()
    with connection:
        row = connection.execute(
            """select message_id, timestamp,sensor_id,
              value, unit from sensor_data limit 1"""
        ).fetchone()
        if row:
            row_id = row[0]
            timestamp = datetime.fromtimestamp(row[1]).isoformat()
            sensor_id = row[2]
            value = row[3]
            unit = row[4]
            try:
                response_code = requests.post(
                    f"{os.getenv('MQTT_BACKEND_URL')}/{sensor_id}",
                    json={
                        "value": math.floor(value),
                        "created_at": timestamp + "Z",
                        "unit": unit,
                    },
                ).status_code
            except requests.exceptions.RequestException:
                response_code = 400

            if response_code == int(os.getenv("MQTT_HTTP_RESPONSE_OK")):
                connection = get_db_connection()
                with connection:
                    connection.execute(
                        "DELETE FROM sensor_data WHERE message_id = ?",
                        (row_id,),
                    )
                _logger.info("sent {value}")


def start_rest_client(stop_event):
    while not stop_event.is_set():
        send_one_value()
