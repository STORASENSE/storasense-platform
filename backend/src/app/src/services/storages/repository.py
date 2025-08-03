from uuid import UUID

from sqlalchemy import Sequence, select
from sqlalchemy.orm import Session

from backend.src.app.src.services.measurements.models import MeasurementModel
from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.shared.repositories.base_repository import (
    BaseRepository,
)


class StorageRepository(BaseRepository[StorageModel, UUID]):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_latest_measurements(
        self, storage_id: UUID, n: int = 100
    ) -> Sequence[MeasurementModel]:
        query = (
            select(MeasurementModel)
            .join(MeasurementModel.sensor)
            .where(SensorModel.storage_id == storage_id)
            .limit(n)
            .order_by(MeasurementModel.created_at.desc())
        )
        return self.session.scalars(query).all()


def inject_storage_repository():
    return None
