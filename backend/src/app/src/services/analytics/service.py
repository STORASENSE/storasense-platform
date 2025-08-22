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
        # already exists in your codebase
        return self._repo.get_sensor_summary(WINDOW_TO_INTERVAL[window])


def inject_analytics_service(
    session: Session = Depends(open_session),
) -> AnalyticsService:
    repo = AnalyticsRepository(session)
    return AnalyticsService(session, repo)
