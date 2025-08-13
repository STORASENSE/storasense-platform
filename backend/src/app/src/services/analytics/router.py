# backend/src/app/src/services/analytics/router.py
from typing import Literal
from fastapi import APIRouter, Depends, Query, status
from backend.src.app.src.services.analytics.service import (
    AnalyticsService,
    inject_analytics_service,
)

Window = Literal["7d", "30d", "365d"]

router = APIRouter(tags=["analytics"])


@router.get("/analytics/summary", status_code=status.HTTP_200_OK)
def get_summary(
    window: Window = Query("7d"),
    svc: AnalyticsService = Depends(inject_analytics_service),
):
    return svc.summary(window)


@router.get("/analytics/door-open-duration", status_code=status.HTTP_200_OK)
def get_door_open_duration(
    window: Window = Query("7d"),
    svc: AnalyticsService = Depends(inject_analytics_service),
):
    # aktuell [] (kein DOOR-Sensor im Schema)
    return svc.door_open_duration(window)
