from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.measurements.models import MeasurementModel
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.pagination import (
    Page,
    PageRequest,
    paginate,
)
from backend.src.app.src.shared.repositories.base_repository import (
    BaseRepository,
)


class MeasurementRepository(BaseRepository[MeasurementModel, UUID]):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_all_by_sensor_id(
        self, sensor_id: UUID, page_request: PageRequest
    ) -> Page[MeasurementModel]:
        query = (
            self.session.query(MeasurementModel)
            .where(MeasurementModel.sensor_id == sensor_id)
            .order_by(MeasurementModel.created_at.desc())
        )
        return paginate(query, page_request)


def inject_measurement_repository(session: Session = Depends(open_session)):
    return MeasurementRepository(session)
