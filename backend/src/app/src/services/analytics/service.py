from __future__ import annotations
from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone
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

    def door_open_duration(self, window: str) -> List[Dict[str, Any]]:
        """
        Returns items {day, sensor_id, open_seconds} for the ULTRASONIC sensor
        in the given window (7d/30d/365d). Matches your frontend shape.
        """
        sid = self._repo.get_ultrasonic_sensor_id()
        if not sid:
            return []

        rows = self._repo.get_door_open_seconds_per_day_window(
            sensor_id=sid,
            window_interval=WINDOW_TO_INTERVAL[window],
            threshold=100.05,  # open if value < threshold
            open_when="lt",
        )

        # GAP-FILL: ensure every day in the window is present
        now = datetime.now(timezone.utc)
        days = {"7d": 7, "30d": 30, "365d": 365}[window]
        start = (now - timedelta(days=days)).date()

        by_day = {r["day"]: r["open_seconds"] for r in rows}
        out: List[Dict[str, Any]] = []
        d = start
        while d <= now.date():
            key = d.isoformat()
            out.append(
                {
                    "day": key,
                    "sensor_id": sid,
                    "open_seconds": by_day.get(key, 0),
                }
            )
            d += timedelta(days=1)
        return out


def inject_analytics_service(
    session: Session = Depends(open_session),
) -> AnalyticsService:
    repo = AnalyticsRepository(session)
    return AnalyticsService(session, repo)
