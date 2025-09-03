import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime

from backend.src.app.src.services.analytics.repository import (
    AnalyticsRepository,
)


class TestAnalyticsRepository:
    @pytest.fixture
    def mock_session(self):
        mock_session = Mock()
        mock_session.query.return_value = mock_session
        return mock_session

    @pytest.fixture
    def analytics_repository(self, mock_session):
        return AnalyticsRepository(mock_session)

    def test_window_start_7_days(self, analytics_repository):
        result = analytics_repository._window_start("7 days")
        assert isinstance(result, datetime)

    def test_window_start_30_days(self, analytics_repository):
        result = analytics_repository._window_start("30 days")
        assert isinstance(result, datetime)

    def test_window_start_365_days(self, analytics_repository):
        result = analytics_repository._window_start("365 days")
        assert isinstance(result, datetime)

    def test_window_start_invalid(self, analytics_repository):
        with pytest.raises(ValueError, match="Unsupported window_interval"):
            analytics_repository._window_start("invalid")

    def test_get_sensor_summary_by_storage(
        self, analytics_repository, mock_session
    ):
        storage_id = uuid4()
        window_interval = "7 days"

        mock_result = Mock()
        mock_result.type = "TEMPERATURE_INSIDE"
        mock_result.sensor_id = uuid4()
        mock_result.avg_value = 22.5
        mock_result.min_value = 18.0
        mock_result.max_value = 27.0

        mock_session.query.return_value.join.return_value.filter.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [
            mock_result
        ]

        result = analytics_repository.get_sensor_summary_by_storage(
            storage_id, window_interval
        )

        assert len(result) == 1
        assert result[0]["type"] == "TEMPERATURE_INSIDE"
        assert result[0]["avg_value"] == 22.5
        assert result[0]["min_value"] == 18.0
        assert result[0]["max_value"] == 27.0

    def test_get_sensor_summary_by_storage_none_values(
        self, analytics_repository, mock_session
    ):
        storage_id = uuid4()
        window_interval = "7 days"

        mock_result = Mock()
        mock_result.type = "HUMIDITY"
        mock_result.sensor_id = uuid4()
        mock_result.avg_value = None
        mock_result.min_value = None
        mock_result.max_value = None

        mock_session.query.return_value.join.return_value.filter.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [
            mock_result
        ]

        result = analytics_repository.get_sensor_summary_by_storage(
            storage_id, window_interval
        )

        assert len(result) == 1
        assert result[0]["type"] == "HUMIDITY"
        assert result[0]["avg_value"] == 0.0
        assert result[0]["min_value"] == 0.0
        assert result[0]["max_value"] == 0.0
