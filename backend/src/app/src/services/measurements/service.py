from datetime import datetime
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.shared.logger import get_logger
from backend.src.app.src.services.measurements.models import MeasurementModel
from backend.src.app.src.services.measurements.repository import (
    MeasurementRepository,
    inject_measurement_repository,
)
from backend.src.app.src.services.measurements.schemas import (
    CreateMeasurementRequest,
)
from backend.src.app.src.services.sensors.errors import SensorDoesNotExistError
from backend.src.app.src.services.sensors.repository import (
    SensorRepository,
    inject_sensor_repository,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.pagination import Page, PageRequest


_logger = get_logger(__name__)


class MeasurementService:
    def __init__(
        self,
        session: Session,
        measurement_repository: MeasurementRepository,
        sensor_repository: SensorRepository,
    ):
        self._session = session
        self._measurement_repository = measurement_repository
        self._sensor_repository = sensor_repository

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
        return self._measurement_repository.find_all_by_sensor_id(
            sensor_id, page_request
        )

    def find_all_by_sensor_id_and_max_date(
        self, sensor_id: UUID, max_date: datetime
    ) -> list[MeasurementModel]:
        _logger.info(
            f"Finding measurements for sensor '{sensor_id}' after date '{max_date}'"
        )

        if not self._sensor_repository.exists(sensor_id):
            _logger.info(f"Requested sensor '{sensor_id}' does not exist!")
            raise SensorDoesNotExistError(
                f"Sensor with ID '{sensor_id}' does not exist"
            )

        result = (
            self._measurement_repository.find_all_by_sensor_id_and_max_date(
                sensor_id, max_date
            )
        )
        _logger.info(f"Found {len(result)} measurements")
        return result

    def create_measurement(
        self, sensor_id: UUID, request: CreateMeasurementRequest
    ):
        """
        Creates a new measurement.
        Condition: The sensor with the given ID must exist.

        :param sensor_id: The ID of the sensor that recorded the measurement.
        :param request: The request for measurement creation.
        """

        sensor = self._sensor_repository.find_by_id(sensor_id)
        if not sensor:
            raise ValueError(f"Sensor with ID {sensor_id} does not exist.")

        measurement = MeasurementModel()
        measurement.sensor_id = sensor_id
        measurement.value = request.value
        measurement.unit = request.unit
        measurement.created_at = request.created_at

        _logger.info(f"Created measurement '{measurement}'")
        self._measurement_repository.create(measurement)
        self._session.commit()


def inject_measurement_service(
    session: Session = Depends(open_session),
    measurement_repository: MeasurementRepository = Depends(
        inject_measurement_repository
    ),
    sensor_repository: SensorRepository = Depends(inject_sensor_repository),
) -> MeasurementService:
    return MeasurementService(
        session, measurement_repository, sensor_repository
    )
