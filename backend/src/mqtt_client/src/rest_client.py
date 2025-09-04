import math
import os
import time
import requests
import urllib3

from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from database import get_db_connection

from logger import get_logger

urllib3.disable_warnings(InsecureRequestWarning)

_logger = get_logger(__name__)

_access_token = None
_token_expires_at = 0


def post_data(token, row):
    timestamp = datetime.fromtimestamp(row[1]).isoformat()
    sensor_id = row[2]
    value = row[3]
    unit = row[4]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    backend_url = os.getenv("MQTT_BACKEND_URL")
    if not backend_url:
        _logger.error("MQTT_BACKEND_URL environment variable not set")
        return
    response = requests.post(
        f"{backend_url}/{sensor_id}",
        headers=headers,
        json={
            "value": math.floor(value),
            "created_at": timestamp + "Z",
            "unit": unit,
        },
    )

    return response


def get_keycloak_config():
    keycloak_url = os.getenv("MQTT_KEYCLOAK_URL")
    realm_name = os.getenv("KEYCLOAK_REALM")
    client_id = os.getenv("MQTT_KEYCLOAK_CLIENT_ID")
    client_secret = os.getenv("MQTT_KEYCLOAK_CLIENT_SECRET")

    if not all([keycloak_url, realm_name, client_id, client_secret]):
        _logger.error(
            f"Missing environment variables: KEYCLOAK_URL={keycloak_url}, REALM={realm_name}, CLIENT_ID={client_id}, CLIENT_SECRET=***"
        )
        raise RuntimeError(
            "Keycloak is not configured correctly. Please check environment variables."
        )

    return keycloak_url, realm_name, client_id, client_secret


def call_me_endpoint(token):
    backend_init_url = os.getenv("MQTT_BACKEND_INIT_URL")
    if not backend_init_url:
        _logger.error("MQTT_BACKEND_INIT_URL environment variable not set")
        return
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{backend_init_url}", headers=headers)
        response.raise_for_status()
        _logger.info(f"/me response: {response.json()}")
    except requests.exceptions.RequestException as e:
        _logger.error(f"Error calling /me endpoint: {e}")


def get_access_token():
    """
    Gets an access token from Keycloak using the client credentials grant flow.
    """
    global _access_token, _token_expires_at

    keycloak_url, realm_name, client_id, client_secret = get_keycloak_config()

    token_url = (
        f"{keycloak_url}/realms/{realm_name}/protocol/openid-connect/token"
    )

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(
            token_url, headers=headers, data=payload, verify=False
        )
        response.raise_for_status()

        token_data = response.json()
        _logger.debug("Token data received successfully.")

        # Store the access token and its expiration time
        _access_token = token_data.get("access_token")
        expires_in = token_data.get("expires_in", 3600)
        _token_expires_at = time.time() + expires_in - 60  # 60 seconds buffer

        # /me-Endpoint calling once after getting the token
        call_me_endpoint(_access_token)

        return _access_token

    except requests.exceptions.RequestException as e:
        _logger.error(f"Error while getting token: {e}")
        return None


def get_valid_token():
    """
    Returns a valid access token, refreshing it if necessary.
    """
    global _access_token, _token_expires_at

    # check if the token is already set and valid
    if not _access_token or time.time() >= _token_expires_at:
        _logger.info("Token expired or missing, requesting new token...")
        _access_token = get_access_token()

    return _access_token


def parse_response(row_id, response):
    response_code = response.status_code
    expected_code = os.getenv("MQTT_HTTP_RESPONSE_OK", "200")
    if response_code == int(expected_code) or response_code == 400:
        connection = get_db_connection()
        with connection:
            connection.execute(
                "DELETE FROM sensor_data WHERE message_id = ?",
                (row_id,),
            )
        if response_code == int(expected_code):
            _logger.info(f"Successfully sent row id {row_id}")
        elif response_code == 400:
            _logger.error(
                f"Bad request when sending row id {row_id} with error {response.text}, deleting from DB"
            )
    else:
        _logger.error(
            f"Failed to send row_id {row_id}, response body {response.text}"
        )
    return response_code


def send_one_value():
    token = get_valid_token()
    if not token:
        _logger.warning(
            "Token was not received. Returning without sending data."
        )
        return -1
    # get one row from the database
    connection = get_db_connection()
    with connection:
        row = connection.execute(
            """select message_id, timestamp, sensor_id, value, unit
               from sensor_data limit 1"""
        ).fetchone()
    if row:
        try:
            # post the data to the backend
            response = post_data(token, row)
        except Exception as e:
            _logger.error(f"Error posting data: {e}")
            return -1
        row_id = row[0]
        return parse_response(row_id, response)

    return 0


def start_rest_client(stop_event):
    while not stop_event.is_set():
        try:
            response_code = send_one_value()
            if (
                response_code != int(os.getenv("MQTT_HTTP_RESPONSE_OK"))
                and response_code != 400
            ):
                time.sleep(5)  # Wait for 5 seconds before retrying
        except Exception as e:
            _logger.error(e)
