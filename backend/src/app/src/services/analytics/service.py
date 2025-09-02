from __future__ import annotations
from uuid import UUID
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

    def summary_by_storage(self, storage_id: UUID, window: str):
        """
        Get sensor summary by storage.

        :param storage_id: Storage ID for which to get the summary
        :param window: Time window (e.g., '7d', '30d', '365d')
        :return: Sensor summary data
        """
        interval = WINDOW_TO_INTERVAL[window]
        return self._repo.get_sensor_summary_by_storage(storage_id, interval)


def inject_analytics_service(
    session: Session = Depends(open_session),
) -> AnalyticsService:
    repo = AnalyticsRepository(session)
    return AnalyticsService(session, repo)
