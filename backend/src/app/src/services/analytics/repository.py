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
