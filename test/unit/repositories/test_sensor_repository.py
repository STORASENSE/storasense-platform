import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.sensors.repository import SensorRepository


class TestSensorRepository:
    @pytest.fixture
    def mock_session(self):
        mock_session = Mock()
        mock_session.query.return_value = mock_session
        mock_session.get.return_value = None
        mock_session.filter.return_value = mock_session
        mock_session.all.return_value = []
        mock_session.add = Mock()
        return mock_session

    @pytest.fixture
    def sensor_repository(self, mock_session):
        return SensorRepository(mock_session)

    def test_find_by_id_success(self, sensor_repository, mock_session):
        sensor_id = uuid4()
        expected_sensor = Mock()

        mock_session.get.return_value = expected_sensor

        result = sensor_repository.find_by_id(sensor_id)

        assert result == expected_sensor
        mock_session.get.assert_called_once_with(sensor_id)

    def test_find_by_id_not_found(self, sensor_repository, mock_session):
        sensor_id = uuid4()

        mock_session.get.return_value = None

        result = sensor_repository.find_by_id(sensor_id)

        assert result is None

    def test_find_all_by_storage_id(self, sensor_repository, mock_session):
        storage_id = uuid4()
        expected_sensors = [Mock(), Mock()]

        mock_session.where.return_value = mock_session
        mock_session.all.return_value = expected_sensors

        result = sensor_repository.find_all_by_storage_id(storage_id)

        assert result == expected_sensors
