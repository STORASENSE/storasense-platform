import os
from rest_auth import get_valid_token
import requests


def get_request(endpoint: str):
    (
        """
    Sends a GET request to the given endpoint and returns the response.
    """
        ""
    )
    url = os.getenv("TEST_BACKEND_URL")
    if not url or not endpoint:
        raise RuntimeError("TEST_BACKEND_URL or endpoint not set")
    token = get_valid_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return requests.get(
        f"{url}{endpoint}", headers=headers, verify=False
    ).json()


def check_mqtt():
    """
    Checks if the MQTT client sent the correct data
    """
    storages = get_request("storages/myStorages")
    print(storages)
