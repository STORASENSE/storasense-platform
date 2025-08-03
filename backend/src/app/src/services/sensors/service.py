from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.sensors.repository import (
    SensorRepository,
    inject_sensor_repository,
)
from backend.src.app.src.services.storages.repository import (
    StorageRepository,
    inject_storage_repository,
)
from backend.src.app.src.shared.database.engine import open_session


class SensorService:
    def __init__(
        self,
        session: Session,
        sensor_repository: SensorRepository,
        storage_repository: StorageRepository,
    ):
        self._session = session
        self._sensor_repository = sensor_repository
        self._storage_repository = storage_repository

    def find_sensor_by_id(self, sensor_id: UUID) -> SensorModel:
        """Finds a sensor by its ID."""
        return self._sensor_repository.find_by_id(sensor_id)

    def create_sensor(self, sensor_id: UUID, request):
        """
        Creates a new sensor.
        Condition: The sensor with the given ID must not exist.
        Condition_2: The storage with the given ID must exist.

        :param sensor_id: The ID of the sensor to be created.
        :param request: The request for sensor creation.
        """
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if sensor:
            raise ValueError(f"Sensor with ID {sensor_id} already exists.")

        storage = self._sensor_repository.find_by_id(request.storage_id)
        if not storage:
            raise ValueError(f"Storage with ID {sensor_id} does not exist.")

        sensor = SensorModel()
        sensor.id = sensor_id
        sensor.type = request.type
        sensor.storage_id = request.storage_id
        sensor.storage = request.storage

        self._sensor_repository.create(sensor)
        self._session.commit()


def inject_sensor_service(
    session: Session = Depends(open_session),
    sensor_repository: SensorRepository = Depends(inject_sensor_repository),
    storage_repository: StorageRepository = Depends(inject_storage_repository),
) -> SensorService:
    return SensorService(session, sensor_repository, storage_repository)
