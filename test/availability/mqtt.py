from test.rest_functionality.rest_methods import get_request


def check_mqtt():
    """
    Checks if the MQTT client sent the correct data
    """
    storages = get_request("storages/byUserId/")
    print(storages)
