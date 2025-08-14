from __future__ import annotations
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session


class AnalyticsRepository:
    def __init__(self, session: Session):
        self._session = session

    # already existing:
    # def get_sensor_summary(self, window_interval: str): ...

    def get_ultrasonic_sensor_id(self) -> Optional[str]:
        """
        Returns the first ULTRASONIC sensor id; falls back to name 'Ultrasonic'.
        """
        row = self._session.execute(
            text(
                'SELECT id FROM "Sensor" WHERE type = :t ORDER BY name LIMIT 1'
            ),
            {"t": "ULTRASONIC"},
        ).first()
        if row:
            return str(row[0])
        row = self._session.execute(
            text(
                'SELECT id FROM "Sensor" WHERE name ILIKE :n ORDER BY name LIMIT 1'
            ),
            {"n": "ultrasonic%"},
        ).first()
        return str(row[0]) if row else None

    def get_door_open_seconds_per_day_window(
        self,
        sensor_id: str,
        window_interval: str,  # e.g. '7 days'
        threshold: float = 100.05,  # default fits your seed data
        open_when: str = "lt",  # 'lt' => value < threshold, 'gt' => value > threshold
    ) -> List[Dict[str, Any]]:
        """
        Computes daily 'open seconds' within [now()-window, now()].
        Uses LEAD() + day-splitting for exact per-day sums.
        """
        comparator = "<" if open_when == "lt" else ">"
        sql = text(
            f"""
        WITH bounds AS (
          SELECT now() - (:win)::interval AS start_ts, now() AS end_ts
        ),
        w AS (
          SELECT
            m.created_at AS ts,
            CASE WHEN m.value {comparator} :thr THEN 1 ELSE 0 END AS val,
            LEAD(m.created_at) OVER (ORDER BY m.created_at) AS next_ts
          FROM "Measurements" m
          CROSS JOIN bounds b
          WHERE m.sensor_id = :sid
            AND m.created_at >= b.start_ts
            AND m.created_at <= b.end_ts
        ),
        intervals AS (
          SELECT ts, COALESCE(next_ts, (SELECT end_ts FROM bounds)) AS next_ts, val
          FROM w
          WHERE next_ts IS NOT NULL
        ),
        split AS (
          SELECT
            date_trunc('day', ts)::date AS day,
            GREATEST(ts, day_start) AS seg_start,
            LEAST(next_ts, day_start + interval '1 day') AS seg_end,
            val
          FROM intervals
          CROSS JOIN LATERAL generate_series(
            date_trunc('day', ts),
            date_trunc('day', next_ts),
            interval '1 day'
          ) AS day_start
          WHERE next_ts > ts
        )
        SELECT
          day,
          SUM(CASE WHEN val=1 THEN EXTRACT(EPOCH FROM (seg_end - seg_start)) ELSE 0 END)::bigint AS open_seconds
        FROM split
        GROUP BY day
        ORDER BY day;
        """
        )
        rows = (
            self._session.execute(
                sql,
                {"sid": sensor_id, "win": window_interval, "thr": threshold},
            )
            .mappings()
            .all()
        )
        return [
            {
                "day": r["day"].isoformat(),
                "open_seconds": int(r["open_seconds"] or 0),
            }
            for r in rows
        ]

    def get_sensor_summary(self, window_interval: str) -> List[Dict[str, Any]]:
        """
        Returns per-sensor min/avg/max for the given window.
        Shape matches your frontend:
        [{ type: str, sensor_id: str, avg_value: float, min_value: float, max_value: float }]
        """
        sql = text(
            """
                   SELECT s.type       AS type,
                          m.sensor_id  AS sensor_id,
                          AVG(m.value) AS avg_value,
                          MIN(m.value) AS min_value,
                          MAX(m.value) AS max_value
                   FROM "Measurements" m
                            JOIN "Sensor" s ON s.id = m.sensor_id
                   WHERE m.created_at >= now() - (:win)::interval
                   GROUP BY s.type, m.sensor_id
                   ORDER BY s.type, m.sensor_id
                   """
        )
        rows = (
            self._session.execute(sql, {"win": window_interval})
            .mappings()
            .all()
        )
        # Ensure types are plain Python types
        return [
            {
                "type": r["type"],
                "sensor_id": str(r["sensor_id"]),
                "avg_value": (
                    float(r["avg_value"])
                    if r["avg_value"] is not None
                    else 0.0
                ),
                "min_value": (
                    float(r["min_value"])
                    if r["min_value"] is not None
                    else 0.0
                ),
                "max_value": (
                    float(r["max_value"])
                    if r["max_value"] is not None
                    else 0.0
                ),
            }
            for r in rows
        ]
