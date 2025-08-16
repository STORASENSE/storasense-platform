from __future__ import annotations
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.measurements.models import MeasurementModel


class AnalyticsRepository:
    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def _window_start(window_interval: str) -> datetime:
        """
        Map a human window string ('7 days' | '30 days' | '365 days') to a UTC start timestamp.
        """
        days_map = {"7 days": 7, "30 days": 30, "365 days": 365}
        days = days_map.get(window_interval)
        if not days:
            raise ValueError(
                f"Unsupported window_interval '{window_interval}'"
            )
        return datetime.now(timezone.utc) - timedelta(days=days)

    @staticmethod
    def _is_open(value: float, threshold: float, when: str) -> bool:
        """
        Decide if the door is "open" for a measurement value using a threshold.
        when='lt' -> open if value < threshold
        when='gt' -> open if value > threshold
        """
        return value < threshold if when == "lt" else value > threshold

    def get_ultrasonic_sensor_id(self) -> Optional[str]:
        row = (
            self._session.query(SensorModel.id)
            .filter(SensorModel.type == "ULTRASONIC")
            .order_by(SensorModel.name.asc())
            .limit(1)
            .first()
        )
        if row:
            return str(row[0])

        row = (
            self._session.query(SensorModel.id)
            .filter(func.lower(SensorModel.name).like("ultrasonic%"))
            .order_by(SensorModel.name.asc())
            .limit(1)
            .first()
        )
        return str(row[0]) if row else None

    def get_sensor_summary(self, window_interval: str) -> List[Dict[str, Any]]:
        """
        Per-sensor MIN/AVG/MAX for the given window.
        Shape matches the frontend:
        [{ type: str, sensor_id: str, avg_value: float, min_value: float, max_value: float }]
        """
        start_ts = self._window_start(window_interval)

        rows = (
            self._session.query(
                SensorModel.type.label("type"),
                MeasurementModel.sensor_id.label("sensor_id"),
                func.avg(MeasurementModel.value).label("avg_value"),
                func.min(MeasurementModel.value).label("min_value"),
                func.max(MeasurementModel.value).label("max_value"),
            )
            .join(SensorModel, SensorModel.id == MeasurementModel.sensor_id)
            .filter(MeasurementModel.created_at >= start_ts)
            .group_by(SensorModel.type, MeasurementModel.sensor_id)
            .order_by(SensorModel.type.asc(), MeasurementModel.sensor_id.asc())
            .all()
        )

        out: List[Dict[str, Any]] = []
        for r in rows:
            out.append(
                {
                    "type": r.type,
                    "sensor_id": str(r.sensor_id),
                    "avg_value": (
                        float(r.avg_value) if r.avg_value is not None else 0.0
                    ),
                    "min_value": (
                        float(r.min_value) if r.min_value is not None else 0.0
                    ),
                    "max_value": (
                        float(r.max_value) if r.max_value is not None else 0.0
                    ),
                }
            )
        return out

    def get_door_open_seconds_per_day_window(
        self,
        sensor_id: str,
        window_interval: str,  # '7 days' | '30 days' | '365 days'
        threshold: float = 100.05,  # open if value < threshold (default)
        open_when: str = "lt",  # 'lt' or 'gt'
    ) -> List[Dict[str, Any]]:
        """
        Approach:
          1) Load measurements for the sensor within the window, ascending by timestamp.
          2) For each point, attribute the time until the next point (or window end) to the
             current state (open/closed) based on threshold comparison.
          3) Split intervals across day boundaries in Python and accumulate seconds per day.

        Returns:
          [{ "day": "YYYY-MM-DD", "open_seconds": int }, ...]  (days present only if any open seconds)
        Note:
          The service layer already "gap-fills" all days to include zeroes.
        """
        start_ts = self._window_start(window_interval)
        end_ts = datetime.now(timezone.utc)

        rows = (
            self._session.query(
                MeasurementModel.created_at, MeasurementModel.value
            )
            .filter(MeasurementModel.sensor_id == sensor_id)
            .filter(MeasurementModel.created_at >= start_ts)
            .filter(MeasurementModel.created_at <= end_ts)
            .order_by(MeasurementModel.created_at.asc())
            .all()
        )

        if not rows:
            return []

        per_day_seconds: Dict[str, int] = {}

        def add_interval_split_by_day(t0: datetime, t1: datetime) -> None:
            """
            Add [t0, t1) seconds to the correct day buckets, splitting at midnight boundaries.
            """
            if t1 <= t0:
                return
            cur = t0
            while cur < t1:
                day_start = datetime(
                    cur.year, cur.month, cur.day, tzinfo=cur.tzinfo
                )
                day_end = day_start + timedelta(days=1)
                seg_end = t1 if t1 <= day_end else day_end
                seconds = int((seg_end - cur).total_seconds())
                key = day_start.date().isoformat()
                per_day_seconds[key] = per_day_seconds.get(key, 0) + max(
                    seconds, 0
                )
                cur = seg_end

        for idx, (ts, val) in enumerate(rows):
            next_ts = rows[idx + 1][0] if idx + 1 < len(rows) else end_ts
            if self._is_open(float(val), threshold, open_when):
                add_interval_split_by_day(ts, next_ts)

        return [
            {"day": day_iso, "open_seconds": secs}
            for day_iso, secs in sorted(per_day_seconds.items())
        ]
