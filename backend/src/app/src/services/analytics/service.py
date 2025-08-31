from __future__ import annotations
from sqlalchemy.orm import Session
from fastapi import Depends

from backend.src.app.src.services.analytics.repository import (
    AnalyticsRepository,
)
from backend.src.app.src.shared.database.engine import open_session

WINDOW_TO_INTERVAL = {"7d": "7 days", "30d": "30 days", "365d": "365 days"}


class AnalyticsService:
    def __init__(self, session: Session, repo: AnalyticsRepository):
        self._session = session
        self._repo = repo

    def summary(self, window: str):
        """
        Get summary of sensor data over a specified time window.

        :param window: str: Time window for the summary
        :return: List[Dict]: Summary data for the specified window
        """
        return self._repo.get_sensor_summary(WINDOW_TO_INTERVAL[window])

    def summary_by_sensor(self, sensor_id, window):
        """
        Get summary of sensor data for a specific sensor over a specified time window.
        :param sensor_id: the sensor id to get the summary for
        :param window: the time window for the summary
        :return: List[Dict]: Summary data for the specified sensor and window
        """
        sid = str(sensor_id)
        items = self._repo.get_sensor_summary(WINDOW_TO_INTERVAL[window])
        return [it for it in items if it.get("sensor_id") == sid]


def inject_analytics_service(
    session: Session = Depends(open_session),
) -> AnalyticsService:
    repo = AnalyticsRepository(session)
    return AnalyticsService(session, repo)
