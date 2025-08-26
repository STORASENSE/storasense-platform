import os

import requests

from test.rest_functionality.rest_auth import get_valid_token


def get_request(endpoint: str, parameters: dict = None):
    """
    Sends a GET request to the given endpoint and returns the response.
    """
    url = os.getenv("TEST_BACKEND_URL")
    if parameters is not None:
        endpoint = (
            f"{endpoint}?{'&'.join(f'{k}={v}' for k, v in parameters.items())}"
        )
    endpoint = endpoint.replace("?&", "?")
    if not url or not endpoint:
        raise RuntimeError("TEST_BACKEND_URL or endpoint not set")
    token = get_valid_token()
    print("token", token)
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{url}{endpoint}", headers=headers, verify=False)


def post_request(endpoint: str, body: dict):
    """
    Sends a POST request to the given endpoint with the given body and returns the response.
    """
    url = os.getenv("TEST_BACKEND_URL")
    if not url or not endpoint:
        raise RuntimeError("TEST_BACKEND_URL or endpoint not set")
    token = get_valid_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return requests.post(
        f"{url}{endpoint}", json=body, headers=headers, verify=False
    ).json()


def delete_request(endpoint: str):
    """
    Sends a DELETE request to the given endpoint and returns the response.
    """
    url = os.getenv("TEST_BACKEND_URL")
    if not url or not endpoint:
        raise RuntimeError("TEST_BACKEND_URL or endpoint not set")
    token = get_valid_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return requests.delete(
        f"{url}{endpoint}", headers=headers, verify=False
    ).json()
