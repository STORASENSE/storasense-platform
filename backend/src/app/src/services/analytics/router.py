from typing import Literal, List
from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from backend.src.app.src.services.analytics.service import (
    AnalyticsService,
    inject_analytics_service,
)

router = APIRouter(tags=["Analytics"])
Window = Literal["7d", "30d", "365d"]


class DoorOpenItem(BaseModel):
    day: str
    sensor_id: str
    open_seconds: int


@router.get(
    "/analytics/door-open-duration",
    response_model=List[DoorOpenItem],
    status_code=status.HTTP_200_OK,
)
def door_open_duration(
    window: Window = Query("7d"),
    svc: AnalyticsService = Depends(inject_analytics_service),
):
    return svc.door_open_duration(window)


class SummaryItem(BaseModel):
    type: str
    sensor_id: str
    avg_value: float
    min_value: float
    max_value: float


@router.get(
    "/analytics/summary",
    response_model=List[SummaryItem],
    status_code=status.HTTP_200_OK,
)
def analytics_summary(
    window: Window = Query("7d"),
    svc: AnalyticsService = Depends(inject_analytics_service),
):
    # Calls your service.summary(window) -> repo.get_sensor_summary(...)
    return svc.summary(window)
