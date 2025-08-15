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
from backend.src.app.src.services.measurements.service import (
    inject_measurement_service,
)
from backend.src.app.src.shared.database.engine import open_session


class SensorService:
    def __init__(
        self,
        session: Session,
        sensor_repository: SensorRepository,
        storage_repository: StorageRepository,
    ):
        self._measurement_service = inject_measurement_service(
            session, sensor_repository=sensor_repository
        )
        self._session = session
        self._sensor_repository = sensor_repository
        self._storage_repository = storage_repository

    def check_sensor_status(
        self, sensor_id: UUID, max_age_minutes: int = 1
    ) -> dict:
        """
        Checks if a sensor is online based on the last measurement.

        :param sensor_id: The ID of the sensor to check.
        :param max_age_minutes: Maximum age in minutes for a measurement to be considered "online".
        :return: Dictionary with sensor status information.
        """
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if not sensor:
            raise ValueError(f"Sensor with ID {sensor_id} does not exist.")

        # Get last measurement for additional info
        last_measurement = self._measurement_service.find_latest_by_sensor_id(
            sensor_id, max_age_minutes
        )

        is_online = last_measurement is not None

        return {
            "sensor_id": str(sensor_id),
            "is_online": is_online,
            "last_measurement": (
                last_measurement.created_at if last_measurement else None
            ),
        }

    def find_sensor_by_id(self, sensor_id: UUID) -> SensorModel:
        """Finds a sensor by its ID."""
        return self._sensor_repository.find_by_id(sensor_id)

    def find_sensors_by_storage_id(
        self, storage_id: UUID
    ) -> list[SensorModel]:
        storage = self._storage_repository.find_by_id(storage_id)
        if not storage:
            raise ValueError(f"Storage with ID {storage} does not exist.")
        return self._sensor_repository.find_all_by_storage_id(storage_id)

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

        storage = self._storage_repository.find_by_id(request.storage_id)
        if not storage:
            raise ValueError(f"Storage with ID {sensor_id} does not exist.")

        sensor = SensorModel()
        sensor.id = sensor_id
        sensor.type = request.type
        sensor.storage_id = request.storage_id
        sensor.name = request.name
        sensor.allowed_min = request.allowed_min
        sensor.allowed_max = request.allowed_max

        self._sensor_repository.create(sensor)
        self._session.commit()

    def delete_sensor(self, sensor_id: UUID):
        """
        Deletes a sensor by its ID.
        Condition: The sensor with the given ID must exist.

        :param sensor_id: The ID of the sensor to be deleted.
        """
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if not sensor:
            raise ValueError(f"Sensor with ID {sensor_id} does not exist.")

        self._sensor_repository.delete(sensor)
        self._session.commit()


def inject_sensor_service(
    session: Session = Depends(open_session),
    sensor_repository: SensorRepository = Depends(inject_sensor_repository),
    storage_repository: StorageRepository = Depends(inject_storage_repository),
) -> SensorService:
    return SensorService(session, sensor_repository, storage_repository)
