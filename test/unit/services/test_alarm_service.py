import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.alarms.service import AlarmService
from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
    UnknownAuthPrincipalError,
)
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.shared.database.enums import UserRole
from backend.src.app.src.shared.database.pagination import PageRequest, Page


class TestAlarmService:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def mock_alarm_repository(self):
        return Mock()

    @pytest.fixture
    def mock_storage_repository(self):
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
    def alarm_service(
        self,
        mock_session,
        mock_alarm_repository,
        mock_storage_repository,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
    ):
        return AlarmService(
            mock_session,
            mock_alarm_repository,
            mock_storage_repository,
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

    def test_find_alarm_by_id_success(
        self,
        alarm_service,
        mock_alarm_repository,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        alarm_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        sensor_id = uuid4()

        mock_alarm = Mock()
        mock_alarm.sensor_id = sensor_id
        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id
        mock_user = Mock()
        mock_user.id = user_id

        mock_alarm_repository.find_by_id.return_value = mock_alarm
        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )

        result = alarm_service.find_alarm_by_id(alarm_id, token_data)

        assert result == mock_alarm
        mock_alarm_repository.find_by_id.assert_called_once_with(alarm_id)
        mock_user_repository.find_by_keycloak_id.assert_called_once_with(
            token_data.id
        )

    def test_find_alarm_by_id_alarm_not_found(
        self, alarm_service, mock_alarm_repository, token_data
    ):
        alarm_id = uuid4()
        mock_alarm_repository.find_by_id.return_value = None

        with pytest.raises(
            ValueError, match=f"Alarm with ID {alarm_id} does not exist"
        ):
            alarm_service.find_alarm_by_id(alarm_id, token_data)

    def test_find_alarm_by_id_user_not_found(
        self,
        alarm_service,
        mock_alarm_repository,
        mock_sensor_repository,
        mock_user_repository,
        token_data,
    ):
        alarm_id = uuid4()
        sensor_id = uuid4()

        mock_alarm = Mock()
        mock_alarm.sensor_id = sensor_id
        mock_sensor = Mock()

        mock_alarm_repository.find_by_id.return_value = mock_alarm
        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_repository.find_by_keycloak_id.return_value = None

        with pytest.raises(UnknownAuthPrincipalError):
            alarm_service.find_alarm_by_id(alarm_id, token_data)

    def test_find_alarm_by_id_unauthorized_user(
        self,
        alarm_service,
        mock_alarm_repository,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        alarm_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        sensor_id = uuid4()

        mock_alarm = Mock()
        mock_alarm.sensor_id = sensor_id
        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id
        mock_user = Mock()
        mock_user.id = user_id

        mock_alarm_repository.find_by_id.return_value = mock_alarm
        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = None

        with pytest.raises(AuthorizationError):
            alarm_service.find_alarm_by_id(alarm_id, token_data)

    def test_delete_alarm_success(
        self,
        alarm_service,
        mock_session,
        mock_alarm_repository,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        alarm_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        sensor_id = uuid4()

        mock_alarm = Mock()
        mock_alarm.sensor_id = sensor_id
        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id
        mock_user = Mock()
        mock_user.id = user_id

        mock_alarm_repository.find_by_id.return_value = mock_alarm
        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )

        alarm_service.delete_alarm(alarm_id, token_data)

        mock_alarm_repository.delete.assert_called_once_with(mock_alarm)
        mock_session.commit.assert_called_once()

    def test_delete_alarm_not_admin(
        self,
        alarm_service,
        mock_alarm_repository,
        mock_sensor_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        alarm_id = uuid4()
        storage_id = uuid4()
        user_id = uuid4()
        sensor_id = uuid4()

        mock_alarm = Mock()
        mock_alarm.sensor_id = sensor_id
        mock_sensor = Mock()
        mock_sensor.storage_id = storage_id
        mock_user = Mock()
        mock_user.id = user_id

        mock_alarm_repository.find_by_id.return_value = mock_alarm
        mock_sensor_repository.find_by_id.return_value = mock_sensor
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.CONTRIBUTOR
        )

        with pytest.raises(AuthorizationError):
            alarm_service.delete_alarm(alarm_id, token_data)

    def test_find_alarms_by_storage_id_success(
        self,
        alarm_service,
        mock_storage_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
        mock_alarm_repository,
        token_data,
    ):
        storage_id = uuid4()
        user_id = uuid4()
        page_request = PageRequest(page_number=1, page_size=10)

        mock_storage = Mock()
        mock_user = Mock()
        mock_user.id = user_id
        mock_page = Page(items=[], page_size=10, page_number=1, total_pages=0)

        mock_storage_repository.find_by_id.return_value = mock_storage
        mock_user_repository.find_by_keycloak_id.return_value = mock_user
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )
        mock_alarm_repository.find_alarms_by_storage_id.return_value = (
            mock_page
        )

        result = alarm_service.find_alarms_by_storage_id(
            storage_id, page_request, token_data
        )

        assert result == mock_page
        mock_alarm_repository.find_alarms_by_storage_id.assert_called_once_with(
            storage_id, page_request
        )

    def test_find_alarms_by_storage_id_storage_not_found(
        self, alarm_service, mock_storage_repository, token_data
    ):
        storage_id = uuid4()
        page_request = PageRequest(page_number=1, page_size=10)

        mock_storage_repository.find_by_id.return_value = None

        with pytest.raises(
            ValueError, match=f"Storage with ID {storage_id} does not exist"
        ):
            alarm_service.find_alarms_by_storage_id(
                storage_id, page_request, token_data
            )
