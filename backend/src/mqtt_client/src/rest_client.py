import math
import os
from datetime import datetime

import requests
from database import get_db_connection
from backend.src.app.src.shared.logging import logging

_logger = logging.getLogger(__name__)

KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL")
REALM_NAME = os.environ.get("KEYCLOAK_REALM")
CLIENT_ID = os.environ.get("MQTT_KEYCLOAK_CLIENT_ID")
CLIENT_SECRET = os.environ.get("MQTT_KEYCLOAK_CLIENT_SECRET")

if not all([KEYCLOAK_URL, REALM_NAME, CLIENT_ID, CLIENT_SECRET]):
    raise RuntimeError(
        "Keycloak is not configured correctly. Please check environment variables."
    )


# Client credentials grant flow
def get_access_token():
    """
    Gets an access token from Keycloak using the client credentials grant flow.
    """
    token_url = (
        f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
    )

    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()

        token_data = response.json()
        _logger.debug("Token data received successfully.")
        return token_data.get("access_token")

    except requests.exceptions.RequestException as e:
        _logger.debug(f"Error while getting token: {e}")
        return None


def send_one_value(token):
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
                if not token:
                    _logger.warning(
                        "Token was not received. Returning without sending data."
                    )
                    return
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                response_code = requests.post(
                    f"{os.getenv('MQTT_BACKEND_URL')}/{sensor_id}",
                    headers=headers,
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
    access_token = get_access_token()
    if not access_token:
        _logger.error("Failed to obtain access token. Exiting.")
        return
    while not stop_event.is_set():
        send_one_value(access_token)
