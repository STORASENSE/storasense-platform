import pytest
from unittest.mock import Mock
from datetime import datetime
from uuid import uuid4

from backend.src.app.src.services.measurements.service import (
    MeasurementService,
)
from backend.src.app.src.services.measurements.schemas import (
    CreateMeasurementRequest,
)
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
)
from backend.src.app.src.services.sensors.errors import (
    SensorDoesNotExistError,
)
from backend.src.app.src.shared.database.enums import (
    UserRole,
    MeasurementUnit,
)
from backend.src.app.src.shared.database.pagination import Page, PageRequest
from fastapi import HTTPException


class TestMeasurementService:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def mock_measurement_repo(self):
        return Mock()

    @pytest.fixture
    def mock_sensor_repository(self):
        return Mock()

    @pytest.fixture
    def mock_user_repository(self):
        return Mock()

    @pytest.fixture
    def mock_user_storage_access_repository(self):
        return Mock()

    @pytest.fixture
    def measurement_service(
        self,
        mock_session,
        mock_measurement_repo,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
    ):
        return MeasurementService(
            mock_session,
            mock_measurement_repo,
            mock_sensor_repository,
            mock_user_repository,
            mock_user_storage_access_repository,
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

    def test_find_all_by_sensor_id_success(
        self,
        measurement_service,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        mock_measurement_repo,
        token_data,
    ):
        sensor_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        page_request = PageRequest(page_number=1, page_size=10)

        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id
        mock_user = Mock()
        mock_user.id = user_id
        mock_page = Page(items=[], page_size=10, page_number=1, total_pages=0)

        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )
        mock_measurement_repo.find_all_by_sensor_id.return_value = mock_page

        result = measurement_service.find_all_by_sensor_id(
            sensor_id, page_request, token_data
        )

        assert result == mock_page
        mock_measurement_repo.find_all_by_sensor_id.assert_called_once_with(
            sensor_id, page_request
        )

    def test_find_all_by_sensor_id_sensor_not_found(
        self, measurement_service, mock_sensor_repository, token_data
    ):
        sensor_id = uuid4()
        page_request = PageRequest(page_number=1, page_size=10)

        mock_sensor_repository.find_by_id.return_value = None

        with pytest.raises(SensorDoesNotExistError):
            measurement_service.find_all_by_sensor_id(
                sensor_id, page_request, token_data
            )

    def test_find_all_by_sensor_id_unauthorized(
        self,
        measurement_service,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        sensor_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        page_request = PageRequest(page_number=1, page_size=10)

        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id
        mock_user = Mock()
        mock_user.id = user_id

        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = None

        with pytest.raises(AuthorizationError):
            measurement_service.find_all_by_sensor_id(
                sensor_id, page_request, token_data
            )

    def test_find_all_by_sensor_id_and_max_date_success(
        self,
        measurement_service,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        mock_measurement_repo,
        token_data,
    ):
        sensor_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        max_date = datetime.now()

        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id
        mock_user = Mock()
        mock_user.id = user_id
        mock_measurements = [Mock()]

        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.CONTRIBUTOR
        )
        # Setup mock return value
        find_method = mock_measurement_repo.find_all_by_sensor_id_and_max_date
        find_method.return_value = mock_measurements

        result = measurement_service.find_all_by_sensor_id_and_max_date(
            sensor_id, max_date, token_data
        )

        assert result == mock_measurements
        # Verify the mock was called correctly
        mock_method = mock_measurement_repo.find_all_by_sensor_id_and_max_date
        mock_method.assert_called_once_with(sensor_id, max_date)

    def test_create_measurement_success(
        self,
        measurement_service,
        mock_session,
        mock_sensor_repository,
        mock_measurement_repo,
    ):
        sensor_id = uuid4()
        username = "service-account-mqtt-client"
        request = CreateMeasurementRequest(
            value=25.5, unit=MeasurementUnit.CELSIUS, created_at=datetime.now()
        )

        mock_sensor = Mock()
        mock_sensor_repository.find_by_id.return_value = mock_sensor

        measurement_service.create_measurement(sensor_id, request, username)

        mock_measurement_repo.create.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_create_measurement_wrong_username(self, measurement_service):
        sensor_id = uuid4()
        username = "wrong-user"
        request = CreateMeasurementRequest(
            value=25.5, unit=MeasurementUnit.CELSIUS, created_at=datetime.now()
        )

        with pytest.raises(HTTPException) as exc_info:
            measurement_service.create_measurement(
                sensor_id, request, username
            )

        assert exc_info.value.status_code == 403

    def test_create_measurement_sensor_not_found(
        self, measurement_service, mock_sensor_repository
    ):
        sensor_id = uuid4()
        username = "service-account-mqtt-client"
        request = CreateMeasurementRequest(
            value=25.5, unit=MeasurementUnit.CELSIUS, created_at=datetime.now()
        )

        mock_sensor_repository.find_by_id.return_value = None

        with pytest.raises(SensorDoesNotExistError):
            measurement_service.create_measurement(
                sensor_id, request, username
            )
