import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.analytics.service import AnalyticsService


class TestAnalyticsService:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def mock_analytics_repo(self):
        return Mock()

    @pytest.fixture
    def analytics_service(self, mock_session, mock_analytics_repo):
        return AnalyticsService(mock_session, mock_analytics_repo)

    def test_summary_by_storage_7d(
        self, analytics_service, mock_analytics_repo
    ):
        storage_id = uuid4()
        window = "7d"
        expected_result = [
            {
                "type": "TEMPERATURE_INSIDE",
                "sensor_id": str(uuid4()),
                "avg_value": 22.5,
                "min_value": 18.0,
                "max_value": 27.0,
            }
        ]

        mock_analytics_repo.get_sensor_summary_by_storage.return_value = (
            expected_result
        )

        result = analytics_service.summary_by_storage(storage_id, window)

        assert result == expected_result
        mock_analytics_repo.get_sensor_summary_by_storage.assert_called_once_with(
            storage_id, "7 days"
        )

    def test_summary_by_storage_30d(
        self, analytics_service, mock_analytics_repo
    ):
        storage_id = uuid4()
        window = "30d"
        expected_result = []

        mock_analytics_repo.get_sensor_summary_by_storage.return_value = (
            expected_result
        )

        result = analytics_service.summary_by_storage(storage_id, window)

        assert result == expected_result
        mock_analytics_repo.get_sensor_summary_by_storage.assert_called_once_with(
            storage_id, "30 days"
        )

    def test_summary_by_storage_365d(
        self, analytics_service, mock_analytics_repo
    ):
        storage_id = uuid4()
        window = "365d"
        expected_result = [
            {
                "type": "HUMIDITY",
                "sensor_id": str(uuid4()),
                "avg_value": 45.2,
                "min_value": 30.0,
                "max_value": 80.0,
            },
            {
                "type": "TEMPERATURE_OUTSIDE",
                "sensor_id": str(uuid4()),
                "avg_value": 15.8,
                "min_value": -5.0,
                "max_value": 35.0,
            },
        ]

        mock_analytics_repo.get_sensor_summary_by_storage.return_value = (
            expected_result
        )

        result = analytics_service.summary_by_storage(storage_id, window)

        assert result == expected_result
        mock_analytics_repo.get_sensor_summary_by_storage.assert_called_once_with(
            storage_id, "365 days"
        )
