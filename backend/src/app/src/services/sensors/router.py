from uuid import UUID

from fastapi import Depends, APIRouter, status, HTTPException
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
