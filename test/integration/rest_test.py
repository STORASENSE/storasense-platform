import pytest

from test.rest_functionality.rest_methods import (
    get_request,
)
import os
from dotenv import load_dotenv


@pytest.mark.dependency()
def test_login():
    load_dotenv(dotenv_path="../../.env")
    value = get_request("users/me")
    assert (
        value["username"]
        == f"service-account-{os.getenv('TEST_KEYCLOAK_CLIENT_ID').lower()}"
    )


"""
@pytest.mark.dependency()
def test_health():
    value = get_request("health")
    assert value["status"] == "ok"

@pytest.mark.dependency(depends= {"test_health"})
def test_storage():
    load_dotenv(dotenv_path="../../.env")
    old_storages = get_request("storages/myStorages")
    storage_id =create_storage()
    assert any(storage_id)
    delete_request(f"storages/{storage_id}")
    assert old_storages == get_request("storages/myStorages")
    conn =get_database_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT "name" FROM "Storage" WHERE id = %s', (storage_id,))
        assert cursor.fetchone() is None
@pytest.mark.dependency(depends=["test_storage"])
def test_sensors():
    storage_id = create_storage()
    old_sensors = get_request(f"sensors/byStorageId/{storage_id}")
    sensor_id = create_sensor(storage_id)
    assert any(sensor["id"] == sensor_id for sensor in get_request(f"sensors/byStorageId/{storage_id}"))
    delete_request(f"sensors/{sensor_id}")
    assert old_sensors == get_request(f"sensors/byStorageId/{storage_id}")
    conn = get_database_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT "name" FROM "Sensor" WHERE id = %s', (sensor_id,))
        assert cursor.fetchone() is None
    delete_request(f"storages/{storage_id}")

@pytest.mark.dependency(depends=["test_sensors"])
def test_measurements():
    storage_id = create_storage()
    sensor_id = create_sensor(storage_id)
    old_measurements = get_request(f"measurements/{sensor_id}")
    post_request(f"measurements/{sensor_id}", {"value": 42.0,"unit": "CELSIUS","created_at":1682514000})
    assert any(measurement["value"] == 42.0 for measurement in get_request(f"measurements/{sensor_id}"))
    assert len(old_measurements) + 1 == len(get_request(f"measurements/{sensor_id}"))
    delete_request(f"sensors/{sensor_id}")
    delete_request(f"storages/{storage_id}")


"""
