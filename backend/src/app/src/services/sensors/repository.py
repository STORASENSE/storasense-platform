from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.shared.database.pagination import PageRequest, Page
from backend.src.app.src.shared.repositories.base_repository import (
    BaseRepository,
)


class SensorRepository(BaseRepository[SensorModel, UUID]):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_by_id(self, object_id: UUID) -> Optional[SensorModel]:
        return self.session.query(SensorModel).get(object_id)

    def find_all(self, page_request: PageRequest) -> Page[SensorModel]:
        return self.session.query(SensorModel).all()
