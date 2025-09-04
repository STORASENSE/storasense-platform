from __future__ import annotations
from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.measurements.models import MeasurementModel


class AnalyticsRepository:
    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def _window_start(window_interval: str) -> datetime:
        days_map = {"7 days": 7, "30 days": 30, "365 days": 365}
        days = days_map.get(window_interval)
        if not days:
            raise ValueError(
                f"Unsupported window_interval '{window_interval}'"
            )
        return datetime.now(timezone.utc) - timedelta(days=days)

    def get_sensor_summary_by_storage(
        self, storage_id: UUID, window_interval: str
    ) -> List[Dict[str, Any]]:
        """
        Aggregates MIN/AVG/MAX per sensor for a given storage + time window.
        Shape: [{ type, sensor_id, avg_value, min_value, max_value }]
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
            .filter(SensorModel.storage_id == storage_id)
            .filter(MeasurementModel.timestamp >= start_ts)
            .group_by(SensorModel.type, MeasurementModel.sensor_id)
            .order_by(SensorModel.type.asc(), MeasurementModel.sensor_id.asc())
            .all()
        )

        return [
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
            for r in rows
        ]
