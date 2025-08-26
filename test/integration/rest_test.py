from test.rest_functionality.rest_methods import get_request


def test_login():
    value = get_request("health/")
    assert value == 200
