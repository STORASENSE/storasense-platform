from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.pagination import (
    PageRequest,
    Page,
    paginate,
)
from backend.src.app.src.shared.repositories.base_repository import (
    BaseRepository,
)


class SensorRepository(BaseRepository[SensorModel, UUID]):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_by_id(self, object_id: UUID) -> Optional[SensorModel]:
        return self.session.query(SensorModel).get(object_id)

    def find_all(self, page_request: PageRequest) -> Page[SensorModel]:
        query = self.session.query(SensorModel).order_by(SensorModel.name)
        return paginate(query, page_request)


def inject_sensor_repository(session: Session = Depends(open_session)):
    return SensorRepository(session)
