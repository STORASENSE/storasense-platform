from uuid import UUID
from typing import List

from fastapi import Depends, APIRouter, status, HTTPException

from backend.src.app.src.services.measurements.service import (
    MeasurementService,
    inject_measurement_service,
)
from backend.src.app.src.services.measurements.schemas import (
    CreateMeasurementRequest,
    MeasurementResponse,
)
from backend.src.app.src.shared.database.pagination import PageRequest

router = APIRouter()


@router.get(
    "/measurements/{sensor_id}",
    response_model=List[MeasurementResponse],
    status_code=status.HTTP_200_OK,
)
def find_sensor_measurements(
    sensor_id: UUID,
    measurement_service: MeasurementService = Depends(
        inject_measurement_service
    ),
):
    page_request = PageRequest(0, 100)

    try:
        measurements = measurement_service.find_all_by_sensor_id(
            sensor_id, page_request
        )
        return measurements

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/measurements/{sensor_id}", status_code=status.HTTP_201_CREATED)
def create_measurement(
    sensor_id: UUID,
    request: CreateMeasurementRequest,
    measurement_service: MeasurementService = Depends(
        inject_measurement_service
    ),
):
    try:
        measurement_service.create_measurement(sensor_id, request)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
