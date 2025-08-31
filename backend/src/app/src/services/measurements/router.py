from datetime import datetime
from uuid import UUID
from typing import List

from fastapi import Depends, APIRouter, status, HTTPException

from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.service import auth_service
from backend.src.app.src.shared.logger import get_logger
from backend.src.app.src.services.measurements.service import (
    MeasurementService,
    inject_measurement_service,
)
from backend.src.app.src.services.measurements.schemas import (
    CreateMeasurementRequest,
    MeasurementResponse,
    GetMeasurementsResponse,
)
from backend.src.app.src.services.sensors.errors import SensorDoesNotExistError

from backend.src.app.src.shared.database.pagination import PageRequest

router = APIRouter(tags=["Measurements"])
_logger = get_logger(__name__)


@router.get(
    "/measurements/{sensor_id}",
    response_model=List[MeasurementResponse],
    status_code=status.HTTP_200_OK,
    description="Return latest 100 measurements by sensor ID",
)
def find_sensor_measurements(
    sensor_id: UUID,
    measurement_service: MeasurementService = Depends(
        inject_measurement_service
    ),
    token_data: TokenData = Depends(auth_service.get_current_user),
):
    page_request = PageRequest(0, 100)

    try:
        measurements = measurement_service.find_all_by_sensor_id(
            sensor_id, page_request, token_data
        )
        return measurements

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/measurements/{sensor_id}/filter",
    response_model=GetMeasurementsResponse,
    status_code=status.HTTP_200_OK,
    description="Return measurements by sensor ID and Max-Date",
)
def find_measurements_by_sensor_id_and_max_date(
    sensor_id: UUID,
    max_date: datetime,
    measurement_service: MeasurementService = Depends(
        inject_measurement_service
    ),
    token_data: TokenData = Depends(auth_service.get_current_user),
) -> GetMeasurementsResponse:
    _logger.info("Got HTTP request at '/measurements/{sensor_id}/filter'")
    try:
        result = measurement_service.find_all_by_sensor_id_and_max_date(
            sensor_id, max_date, token_data
        )
    except SensorDoesNotExistError:
        _logger.info("Returning HTTP error due to nonexistent sensor")
        raise HTTPException(
            404, f"Sensor with ID '{sensor_id}' does not exist"
        )

    measurements = [
        MeasurementResponse(
            id=m.id, value=m.value, unit=m.unit, created_at=m.created_at
        )
        for m in result
    ]
    _logger.info(
        f"Returning HTTP response containing {len(measurements)} measurements"
    )
    return GetMeasurementsResponse(measurements=measurements)


@router.post(
    "/measurements/{sensor_id}",
    status_code=status.HTTP_201_CREATED,
    description="Creates a new measurement for a sensor (given by its ID)",
)
async def create_measurement(
    sensor_id: UUID,
    request: CreateMeasurementRequest,
    current_user: TokenData = Depends(auth_service.get_current_user),
    measurement_service: MeasurementService = Depends(
        inject_measurement_service
    ),
):
    try:
        measurement_service.create_measurement(
            sensor_id, request, current_user.username
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
