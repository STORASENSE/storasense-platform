from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter, status, HTTPException

from backend.src.app.src.services.alarms.schemas import (
    AlarmResponse,
)
from backend.src.app.src.services.alarms.service import (
    AlarmService,
    inject_alarm_service,
)
from backend.src.app.src.shared.database.pagination import PageRequest

router = APIRouter()


@router.get("/alarms/{alarm_id}", status_code=status.HTTP_200_OK)
def find_alarm_by_id(
    alarm_id: UUID,
    alarm_service: AlarmService = Depends(inject_alarm_service),
) -> AlarmResponse:
    """Get a specific alarm by its ID."""
    try:
        alarm = alarm_service.find_alarm_by_id(alarm_id)
        if not alarm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alarm with ID {alarm_id} not found.",
            )
        return AlarmResponse(
            id=alarm.id,
            sensor_id=alarm.sensor_id,
            timestamp=alarm.timestamp,
            value=alarm.value,
            message=alarm.message,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/alarms/byStorage/{storage_id}/",
    response_model=List[AlarmResponse],
    status_code=status.HTTP_200_OK,
)
def find_alarms_by_storage_id(
    storage_id: UUID,
    alarm_service: AlarmService = Depends(inject_alarm_service),
):
    """
    Returns latest 50 alarms for a given storage.
    """
    try:
        page_request = PageRequest(1, 50)
        alarms_page = alarm_service.find_alarms_by_storage_id(
            storage_id, page_request
        )
        return [
            AlarmResponse(
                id=alarm.id,
                sensor_id=alarm.sensor_id,
                severity=alarm.severity,
                message=alarm.message,
                created_at=alarm.created_at,
            )
            for alarm in alarms_page.items
        ]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
