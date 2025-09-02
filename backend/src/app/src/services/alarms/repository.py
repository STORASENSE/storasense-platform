from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.src.app.src.services.alarms.models import AlarmModel
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.pagination import (
    PageRequest,
    Page,
)
from backend.src.app.src.shared.database.base_repository import (
    BaseRepository,
)


class AlarmRepository(BaseRepository[AlarmModel, UUID]):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_by_id(self, object_id: UUID) -> Optional[AlarmModel]:
        return self.session.query(AlarmModel).get(object_id)

    def find_alarms_by_storage_id(
        self, storage_id: UUID, page_request: PageRequest
    ) -> Page[dict]:
        sql = text(
            """
            SELECT a.*, s.name AS sensor_name, st.name AS storage_name
            FROM "Alarm" a
                     JOIN "Sensor" s ON a.sensor_id = s.id
                     JOIN "Storage" st ON s.storage_id = st.id
            WHERE s.storage_id = :storage_id
            ORDER BY a.created_at DESC LIMIT :limit_plus_one
            OFFSET :offset
            """
        )

        rows = self.session.execute(
            sql,
            {
                "storage_id": str(storage_id),
                "limit_plus_one": page_request.page_size + 1,
                "offset": (page_request.page_number - 1)
                * page_request.page_size,
            },
        ).all()

        items_data = rows[: page_request.page_size]

        alarm_dicts = []
        for row in items_data:
            alarm_dict = dict(row._mapping)
            alarm_dicts.append(alarm_dict)

        return Page(
            items=alarm_dicts,
            page_size=page_request.page_size,
            page_number=page_request.page_number,
            total_pages=0,
        )


def inject_alarm_repository(session: Session = Depends(open_session)):
    return AlarmRepository(session)
