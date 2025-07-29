from uuid import UUID

from sqlalchemy.orm import Session

from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.shared.repositories.base_repository import (
    BaseRepository,
)


class SensorRepository(BaseRepository[SensorModel, UUID]):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
