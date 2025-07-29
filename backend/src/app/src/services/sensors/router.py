from uuid import UUID

from fastapi import Depends

from backend.src.app.src.main import app
from backend.src.app.src.services.sensors.service import (
    SensorService,
    inject_sensor_service,
)


@app.get("/sensors/{sensor_id}")
def find_sensor_by_id(
    sensor_id: UUID,
    sensor_service: SensorService = Depends(inject_sensor_service),
):
    sensor = sensor_service.find_sensor_by_id(sensor_id)
    return {"id": sensor.id}
