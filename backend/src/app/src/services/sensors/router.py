from uuid import UUID

from fastapi import Depends, APIRouter, status, HTTPException

from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.service import auth_service
from backend.src.app.src.services.sensors.schemas import (
    CreateSensorRequest,
    SensorMetadata,
    SensorStatusResponse,
    DeleteSensorRequest,
)
from backend.src.app.src.services.sensors.service import (
    SensorService,
    inject_sensor_service,
)

router = APIRouter(tags=["Sensors"])


@router.get(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_200_OK,
    description="Gets information about a sensor by its ID.",
)
def find_sensor_by_id(
    sensor_id: UUID,
    token_data: TokenData = Depends(auth_service.get_current_user),
    sensor_service: SensorService = Depends(inject_sensor_service),
):
    try:
        sensor = sensor_service.find_sensor_by_id(sensor_id, token_data)
        return {"id": sensor.id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/sensors/byStorageId/{storage_id}",
    status_code=status.HTTP_200_OK,
    description="Gets a list of sensors associated with a specific storage ID.",
)
def find_sensors_by_storage_id(
    storage_id: UUID,
    token_data: TokenData = Depends(auth_service.get_current_user),
    sensor_service: SensorService = Depends(inject_sensor_service),
) -> list[SensorMetadata]:
    try:
        sensors = sensor_service.find_sensors_by_storage_id(
            storage_id, token_data
        )
        return [
            SensorMetadata(
                id=sensor.id,
                name=sensor.name,
                type=sensor.type,
                allowed_min=sensor.allowed_min,
                allowed_max=sensor.allowed_max,
            )
            for sensor in sensors
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_201_CREATED,
    description="Creates a new sensor with the given ID and metadata for a specific storage.",
)
def create_sensor(
    sensor_id: UUID,
    request: CreateSensorRequest,
    sensor_service: SensorService = Depends(inject_sensor_service),
    token_data: TokenData = Depends(auth_service.get_current_user),
):
    try:
        sensor_service.create_sensor(sensor_id, token_data, request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Deletes a sensor with the given ID from a specific storage.",
)
def delete_sensor(
    sensor_id: UUID,
    request: DeleteSensorRequest,
    sensor_service: SensorService = Depends(inject_sensor_service),
    token_data: TokenData = Depends(auth_service.get_current_user),
):
    try:
        sensor_service.delete_sensor(sensor_id, token_data, request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/sensors/status/{sensor_id}",
    status_code=status.HTTP_200_OK,
    description="Checks the status of a sensor, including its online status (Was a measurement sent at the last minute?).",
)
def check_sensor_status(
    sensor_id: UUID,
    max_age_minutes: int = 1,  # Last minute is important for this check
    token_data: TokenData = Depends(auth_service.get_current_user),
    sensor_service: SensorService = Depends(inject_sensor_service),
):
    try:
        status_info = sensor_service.check_sensor_status(
            sensor_id, max_age_minutes, token_data
        )
        return SensorStatusResponse(**status_info)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
