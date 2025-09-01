from fastapi import APIRouter, status
from datetime import datetime
from backend.src.app.src.services.measurements.schemas import (
    GetMeasurementsResponse,
)

router = APIRouter(prefix="/metadata", tags=["Metadata"])


@router.get(
    "/measurements",
    response_model=GetMeasurementsResponse,
    status_code=status.HTTP_200_OK,
)
def get_measurements_metadata(datetime_from: datetime):
    pass
