import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.alarms.repository import AlarmRepository
from backend.src.app.src.services.alarms.models import AlarmModel
from backend.src.app.src.shared.database.pagination import PageRequest, Page


class TestAlarmRepository:
    @pytest.fixture
    def mock_session(self):
        mock_session = Mock()
        mock_session.query.return_value = mock_session
        mock_session.get.return_value = None
        mock_session.execute.return_value = Mock()
        return mock_session

    @pytest.fixture
    def alarm_repository(self, mock_session):
        return AlarmRepository(mock_session)

    def test_find_by_id_success(self, alarm_repository, mock_session):
        alarm_id = uuid4()
        expected_alarm = Mock(spec=AlarmModel)

        mock_session.get.return_value = expected_alarm

        result = alarm_repository.find_by_id(alarm_id)

        assert result == expected_alarm
        mock_session.get.assert_called_once_with(alarm_id)

    def test_find_by_id_not_found(self, alarm_repository, mock_session):
        alarm_id = uuid4()

        mock_session.get.return_value = None

        result = alarm_repository.find_by_id(alarm_id)

        assert result is None

    def test_find_alarms_by_storage_id(self, alarm_repository, mock_session):
        storage_id = uuid4()
        page_request = PageRequest(page_number=1, page_size=10)

        mock_rows = [
            Mock(
                _mapping={
                    "id": uuid4(),
                    "sensor_name": "Sensor1",
                    "storage_name": "Storage1",
                }
            ),
            Mock(
                _mapping={
                    "id": uuid4(),
                    "sensor_name": "Sensor2",
                    "storage_name": "Storage1",
                }
            ),
        ]

        mock_session.execute.return_value.all.return_value = mock_rows

        result = alarm_repository.find_alarms_by_storage_id(
            storage_id, page_request
        )

        assert isinstance(result, Page)
        assert len(result.items) == 2
        assert result.page_size == 10
        assert result.page_number == 1
        mock_session.execute.assert_called_once()
