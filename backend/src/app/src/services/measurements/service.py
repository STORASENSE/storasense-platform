from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.measurements.models import MeasurementModel
from backend.src.app.src.services.measurements.repository import (
    MeasurementRepository,
    inject_measurement_repository,
)
from backend.src.app.src.services.measurements.schemas import (
    CreateMeasurementRequest,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.pagination import Page, PageRequest


class MeasurementService:
    def __init__(
        self, session: Session, measurement_repository: MeasurementRepository
    ):
        self.session = session
        self.measurement_repository = measurement_repository

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
        return self.measurement_repository.find_all_by_sensor_id(
            sensor_id, page_request
        )

    def create_measurement(
        self, sensor_id: UUID, request: CreateMeasurementRequest
    ):
        """
        Creates a new measurement.

        :param sensor_id: The ID of the sensor that recorded the measurement.
        :param request: The request for measurement creation.
        """
        measurement = MeasurementModel()
        measurement.sensor_id = sensor_id
        measurement.value = request.value
        measurement.unit = request.unit
        measurement.created_at = request.created_at

        self.measurement_repository.create(measurement)
        self.session.commit()


def inject_measurement_service(
    session: Session = Depends(open_session),
    measurement_repository: MeasurementRepository = Depends(
        inject_measurement_repository
    ),
):
    return MeasurementService(session, measurement_repository)
