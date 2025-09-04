import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from uuid import uuid4

from backend.src.app.src.services.sensors.service import SensorService
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
)
from backend.src.app.src.shared.database.enums import UserRole


class TestSensorService:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def mock_sensor_repository(self):
        return Mock()

    @pytest.fixture
    def mock_storage_repository(self):
        return Mock()

    @pytest.fixture
    def mock_measurement_repository(self):
        return Mock()

    @pytest.fixture
    def mock_user_storage_access_repository(self):
        return Mock()

    @pytest.fixture
    def mock_user_repository(self):
        return Mock()

    @pytest.fixture
    def sensor_service(
        self,
        mock_session,
        mock_sensor_repository,
        mock_storage_repository,
        mock_measurement_repository,
        mock_user_storage_access_repository,
        mock_user_repository,
    ):
        return SensorService(
            mock_session,
            mock_sensor_repository,
            mock_storage_repository,
            mock_measurement_repository,
            mock_user_storage_access_repository,
            mock_user_repository,
        )

    @pytest.fixture
    def token_data(self):
        return TokenData(
            id="test-keycloak-id",
            username="testuser",
            email="test@example.com",
            name="Test User",
            client_id="test-client",
        )

    def test_check_sensor_status_online(
        self,
        sensor_service,
        mock_user_repository,
        mock_sensor_repository,
        mock_user_storage_access_repository,
        mock_measurement_repository,
        token_data,
    ):
        sensor_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        max_age_minutes = 10

        mock_user = Mock()
        mock_user.id = user_id
        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id
        mock_measurement = Mock()
        mock_measurement.value = 25.5
        mock_measurement.timestamp = datetime.now(timezone.utc)

        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )
        mock_measurement_repository.find_latest_by_sensor_id.return_value = (
            mock_measurement
        )

        result = sensor_service.check_sensor_status(
            sensor_id, max_age_minutes, token_data
        )

        assert result["sensor_id"] == str(sensor_id)
        assert result["is_online"] is True
        assert result["last_measurement"] == 25.5

    def test_check_sensor_status_offline(
        self,
        sensor_service,
        mock_user_repository,
        mock_sensor_repository,
        mock_user_storage_access_repository,
        mock_measurement_repository,
        token_data,
    ):
        sensor_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        max_age_minutes = 10

        mock_user = Mock()
        mock_user.id = user_id
        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id

        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )
        mock_measurement_repository.find_latest_by_sensor_id.return_value = (
            None
        )

        result = sensor_service.check_sensor_status(
            sensor_id, max_age_minutes, token_data
        )

        assert result["sensor_id"] == str(sensor_id)
        assert result["is_online"] is False
        assert result["last_measurement"] is None

    def test_find_sensor_by_id_success(
        self,
        sensor_service,
        mock_user_repository,
        mock_sensor_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        sensor_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()

        mock_user = Mock()
        mock_user.id = user_id
        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id

        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.CONTRIBUTOR
        )

        result = sensor_service.find_sensor_by_id(sensor_id, token_data)

        assert result == mock_sensor

    def test_find_sensor_by_id_sensor_not_found(
        self,
        sensor_service,
        mock_user_repository,
        mock_sensor_repository,
        token_data,
    ):
        sensor_id = uuid4()
        user_id = uuid4()

        mock_user = Mock()
        mock_user.id = user_id

        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_sensor_repository.find_by_id.return_value = None

        with pytest.raises(
            ValueError, match=f"Sensor with ID {sensor_id} doesnt exist"
        ):
            sensor_service.find_sensor_by_id(sensor_id, token_data)

    def test_find_sensors_by_storage_id_success(
        self,
        sensor_service,
        mock_storage_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        mock_sensor_repository,
        token_data,
    ):
        storage_id = uuid4()
        user_id = uuid4()

        mock_storage = Mock()
        mock_user = Mock()
        mock_user.id = user_id
        mock_sensors = [Mock(), Mock()]

        mock_storage_repository.find_by_id.return_value = mock_storage
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )
        mock_sensor_repository.find_all_by_storage_id.return_value = (
            mock_sensors
        )

        result = sensor_service.find_sensors_by_storage_id(
            storage_id, token_data
        )

        assert result == mock_sensors
        mock_sensor_repository.find_all_by_storage_id.assert_called_once_with(
            storage_id
        )

    def test_find_sensors_by_storage_id_unauthorized(
        self,
        sensor_service,
        mock_storage_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        storage_id = uuid4()
        user_id = uuid4()

        mock_storage = Mock()
        mock_user = Mock()
        mock_user.id = user_id

        mock_storage_repository.find_by_id.return_value = mock_storage
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = None

        with pytest.raises(AuthorizationError):
            sensor_service.find_sensors_by_storage_id(storage_id, token_data)

    @patch.dict("os.environ", {"KAFKA_HOST": "localhost:9092"})
    @patch("backend.src.app.src.services.sensors.service.Producer")
    def test_create_sensor_success(
        self,
        mock_producer_class,
        sensor_service,
        mock_session,
        mock_user_repository,
        mock_user_storage_access_repository,
        mock_sensor_repository,
        mock_storage_repository,
        token_data,
    ):
        sensor_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()

        mock_request = Mock()
        mock_request.storage_id = storage_id
        mock_request.type = "TEMPERATURE_INSIDE"
        mock_request.name = "Test Sensor"
        mock_request.allowed_min = 10.0
        mock_request.allowed_max = 30.0

        mock_user = Mock()
        mock_user.id = user_id
        mock_user.email = "test@example.com"
        mock_storage = Mock()
        mock_producer = Mock()

        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )
        mock_sensor_repository.find_by_id.return_value = None
        mock_storage_repository.find_by_id.return_value = mock_storage
        mock_producer_class.return_value = mock_producer

        sensor_service.create_sensor(sensor_id, token_data, mock_request)

        mock_sensor_repository.create.assert_called_once()
        mock_producer.produce.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_delete_sensor_success(
        self,
        sensor_service,
        mock_session,
        mock_user_repository,
        mock_user_storage_access_repository,
        mock_sensor_repository,
        token_data,
    ):
        sensor_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()

        mock_request = Mock()
        mock_request.storage_id = storage_id
        mock_user = Mock()
        mock_user.id = user_id
        mock_sensor = Mock()

        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )
        mock_sensor_repository.find_by_id.return_value = mock_sensor

        sensor_service.delete_sensor(sensor_id, token_data, mock_request)

        mock_sensor_repository.delete.assert_called_once_with(mock_sensor)
        mock_session.commit.assert_called_once()
