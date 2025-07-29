from uuid import UUID

from fastapi import Depends

from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.sensors.repository import (
    SensorRepository,
    inject_sensor_repository,
)


class SensorService:
    def __init__(self, sensor_repository: SensorRepository):
        self._sensor_repository = sensor_repository

    def find_sensor_by_id(self, sensor_id: UUID) -> SensorModel:
        return self._sensor_repository.find_by_id(sensor_id)


def inject_sensor_service(
    sensor_repository: SensorRepository = Depends(inject_sensor_repository),
) -> SensorService:
    return SensorService(sensor_repository)
