from datetime import datetime
from typing import Optional
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

    def find_by_id(self, object_id: UUID) -> Optional[MeasurementModel]:
        return self.session.query(MeasurementModel).get(object_id)

    def find_all(self, page_request: PageRequest) -> Page[MeasurementModel]:
        query = self.session.query(MeasurementModel).order_by(
            MeasurementModel.created_at.desc()
        )
        return paginate(query, page_request)

    def find_all_by_sensor_id(
        self, sensor_id: UUID, page_request: PageRequest
    ) -> Page[MeasurementModel]:
        """
        Finds all measurements that were recorded by the given sensor. The results are
        ordered from newest to oldest and are stored in a page.

        :param sensor_id: The ID of the sensor whose measurements should be retrieved.
        :param page_request: The pagination request.
        :return: The requested measurements.
        """
        query = (
            self.session.query(MeasurementModel)
            .where(MeasurementModel.sensor_id == sensor_id)
            .order_by(MeasurementModel.created_at.desc())
        )
        return paginate(query, page_request)

    def find_all_by_sensor_id_and_max_date(
        self, sensor_id: UUID, max_date: datetime
    ) -> list[MeasurementModel]:
        query = (
            self.session.query(MeasurementModel)
            .where(MeasurementModel.sensor_id == sensor_id)
            .where(MeasurementModel.created_at <= max_date)
            .order_by(MeasurementModel.created_at.desc())
        )
        return query.all()

    def find_all_by_min_date(
        self, min_date: datetime, page_request: PageRequest
    ) -> Page[MeasurementModel]:
        query = (
            self.session.query(MeasurementModel)
            .where(MeasurementModel.created_at >= min_date)
            .order_by(
                MeasurementModel.sensor_id.desc(),
                MeasurementModel.created_at.desc(),
            )
        )
        return paginate(query, page_request)

    def find_latest_by_sensor_id(
        self, sensor_id: UUID
    ) -> MeasurementModel | None:
        """
        Finds the latest measurement for a given sensor.

        :param sensor_id: The ID of the sensor.
        :return: The latest measurement or None if no measurements exist.
        """
        return (
            self.session.query(MeasurementModel)
            .filter(MeasurementModel.sensor_id == sensor_id)
            .order_by(MeasurementModel.created_at.desc())
            .first()
        )


def inject_measurement_repository(session: Session = Depends(open_session)):
    return MeasurementRepository(session)
