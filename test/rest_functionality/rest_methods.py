import os

import requests

from test.rest_functionality.rest_auth import get_valid_token


def get_request(endpoint: str, parameters: dict = None):
    """
    Sends a GET request to the given endpoint and returns the response.
    """
    url = os.getenv(f"{os.getenv('OPERATING_MODE')}_TEST_BACKEND_URL")
    if parameters is not None:
        endpoint = (
            f"{endpoint}?{'&'.join(f'{k}={v}' for k, v in parameters.items())}"
        )
    endpoint = endpoint.replace("?&", "?")
    if not url or not endpoint:
        raise RuntimeError("TEST_BACKEND_URL or endpoint not set")
    token = get_valid_token()

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}{endpoint}", headers=headers, verify=False)
    if response.status_code > 250:
        raise RuntimeError(
            f"GET {url}{endpoint} failed with status {response.status_code}: {response.text}"
        )
    return response.json()


def post_request(endpoint: str, body: dict):
    """
    Sends a POST request to the given endpoint with the given body and returns the response.
    """
    url = os.getenv(f"{os.getenv('OPERATING_MODE')}_TEST_BACKEND_URL")
    if not url or not endpoint:
        raise RuntimeError("TEST_BACKEND_URL or endpoint not set")
    token = get_valid_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        f"{url}{endpoint}", json=body, headers=headers, verify=False
    )
    if response.status_code > 250:
        raise RuntimeError(
            f"POST {url}{endpoint} failed with status {response.status_code}: {response.text}"
        )
    return response.json()


def delete_request(endpoint: str):
    """
    Sends a DELETE request to the given endpoint and returns the response.
    """
    url = os.getenv(f"{os.getenv('OPERATING_MODE')}_TEST_BACKEND_URL")
    if not url or not endpoint:
        raise RuntimeError("TEST_BACKEND_URL or endpoint not set")
    token = get_valid_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.delete(
        f"{url}{endpoint}", headers=headers, verify=False
    )
    if response.status_code > 250:
        raise RuntimeError(
            f"DELETE {url}{endpoint} failed with status {response.status_code}: {response.text}"
        )
    return response.json() if response.text else {}
