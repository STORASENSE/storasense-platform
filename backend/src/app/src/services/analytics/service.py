# backend/src/app/src/services/analytics/service.py
from sqlalchemy.orm import Session
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
        return self._repo.get_sensor_summary(WINDOW_TO_INTERVAL[window])

    def door_open_duration(self, window: str):
        # Später durch echte Logik ersetzen, wenn DOOR-Sensoren vorhanden sind
        return self._repo.get_door_open_duration_daily_stub()


def inject_analytics_service():
    session: Session = open_session()
    repo = AnalyticsRepository(session)
    return AnalyticsService(session, repo)
