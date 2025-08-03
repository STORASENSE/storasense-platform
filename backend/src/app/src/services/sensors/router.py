from uuid import UUID

from fastapi import Depends, APIRouter, status, HTTPException

from backend.src.app.src.services.sensors.schemas import (
    CreateSensorRequest,
)
from backend.src.app.src.services.sensors.service import (
    SensorService,
    inject_sensor_service,
)

router = APIRouter()


@router.get("/sensors/{sensor_id}", status_code=status.HTTP_200_OK)
def find_sensor_by_id(
    sensor_id: UUID,
    sensor_service: SensorService = Depends(inject_sensor_service),
):
    try:
        sensor = sensor_service.find_sensor_by_id(sensor_id)
        return {"id": sensor.id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/sensors/{sensor_id}", status_code=status.HTTP_201_CREATED)
def create_sensor(
    sensor_id: UUID,
    request: CreateSensorRequest,
    sensor_service: SensorService = Depends(inject_sensor_service),
):
    try:
        sensor_service.create_sensor(sensor_id, request)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
