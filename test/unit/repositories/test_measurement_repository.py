import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.measurements.repository import (
    MeasurementRepository,
)
from backend.src.app.src.services.measurements.models import MeasurementModel


class TestMeasurementRepository:
    @pytest.fixture
    def mock_session(self):
        mock_session = Mock()
        mock_session.query.return_value = mock_session
        mock_session.filter.return_value = mock_session
        mock_session.order_by.return_value = mock_session
        mock_session.all.return_value = []
        mock_session.add = Mock()
        return mock_session

    @pytest.fixture
    def measurement_repository(self, mock_session):
        return MeasurementRepository(mock_session)

    def test_find_by_id_success(self, measurement_repository, mock_session):
        measurement_id = uuid4()
        expected_measurement = Mock(spec=MeasurementModel)

        mock_session.get.return_value = expected_measurement

        result = measurement_repository.find_by_id(measurement_id)

        assert result == expected_measurement

    def test_find_by_id_not_found(self, measurement_repository, mock_session):
        measurement_id = uuid4()

        mock_session.get.return_value = None

        result = measurement_repository.find_by_id(measurement_id)

        assert result is None
