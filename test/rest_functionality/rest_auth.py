import os
import time
import requests
import urllib3

from urllib3.exceptions import InsecureRequestWarning


import logging

urllib3.disable_warnings(InsecureRequestWarning)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

_access_token = None
_token_expires_at = 0


def get_keycloak_config():
    operating_mode = os.getenv("OPERATING_MODE")
    if not operating_mode:
        raise RuntimeError("OPERATING_MODE environment variable not set")
    keycloak_url = os.getenv(f"{operating_mode}_TEST_KEYCLOAK_URL")
    realm_name = os.getenv("KEYCLOAK_REALM")
    client_id = os.getenv("TEST_KEYCLOAK_CLIENT_ID")
    client_secret = os.getenv("TEST_KEYCLOAK_CLIENT_SECRET")

    if not all([keycloak_url, realm_name, client_id, client_secret]):
        _logger.error(
            f"Missing environment variables: KEYCLOAK_URL={keycloak_url}, REALM={realm_name}, CLIENT_ID={client_id}, CLIENT_SECRET=***"
        )
        raise RuntimeError(
            "Keycloak is not configured correctly. Please check environment variables."
        )

    return keycloak_url, realm_name, client_id, client_secret


def call_me_endpoint(token):
    backend_init_url = os.getenv(
        f"{os.getenv('OPERATING_MODE')}_TEST_BACKEND_INIT_URL"
    )
    if not backend_init_url:
        _logger.error("TEST_BACKEND_INIT_URL environment variable not set")
        return
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{backend_init_url}", headers=headers, verify=False
        )
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
