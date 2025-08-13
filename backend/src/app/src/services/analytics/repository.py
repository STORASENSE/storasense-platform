# backend/src/app/src/services/analytics/repository.py
from sqlalchemy import text
from sqlalchemy.orm import Session


class AnalyticsRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_sensor_summary(self, interval: str):
        sql = text(
            """
            SELECT s.type,
                   m."sensor_id",
                   AVG(m.value) AS avg_value,
                   MIN(m.value) AS min_value,
                   MAX(m.value) AS max_value
            FROM "Measurements" m
            JOIN "Sensor" s ON s.id = m."sensor_id"
            WHERE m.created_at >= NOW() - (:interval::INTERVAL)
            GROUP BY s.type, m."sensor_id"
            ORDER BY s.type, m."sensor_id"
        """
        )
        return (
            self._session.execute(sql, {"interval": interval}).mappings().all()
        )

    # Solange es keinen DOOR-Sensor gibt, liefern wir eine leere Liste zurück.
    def get_door_open_duration_daily_stub(self):
        return []
