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
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.service import auth_service
from backend.src.app.src.shared.database.pagination import PageRequest

router = APIRouter(tags=["Alarms"])


@router.get(
    "/alarms/{alarm_id}",
    status_code=status.HTTP_200_OK,
    description="Gets a specific alarm by its ID.",
)
def find_alarm_by_id(
    alarm_id: UUID,
    alarm_service: AlarmService = Depends(inject_alarm_service),
    token_data: TokenData = Depends(auth_service.get_current_user),
) -> AlarmResponse:
    """Get a specific alarm by its ID."""
    try:
        alarm = alarm_service.find_alarm_by_id(alarm_id, token_data)
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
    "/alarms/byStorageId/{storage_id}/",
    response_model=List[AlarmResponse],
    status_code=status.HTTP_200_OK,
    description="Gets latest 50 alarms for a given storage.",
)
def find_alarms_by_storage_id(
    storage_id: UUID,
    alarm_service: AlarmService = Depends(inject_alarm_service),
    token_data: TokenData = Depends(auth_service.get_current_user),
):
    """
    Returns latest 50 alarms for a given storage.
    """
    try:
        page_request = PageRequest(1, 50)
        alarms_page = alarm_service.find_alarms_by_storage_id(
            storage_id, page_request, token_data
        )
        return [
            AlarmResponse(
                id=alarm.id,
                sensor_id=alarm.sensor_id,
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


@router.delete(
    "/alarms/{alarm_id}",
    status_code=status.HTTP_200_OK,
    description="Deletes a specific alarm by its ID.",
)
def delete_alarm(
    alarm_id: UUID,
    token_data: TokenData = Depends(auth_service.get_current_user),
    alarm_service: AlarmService = Depends(inject_alarm_service),
) -> None:
    """Delete a specific alarm by its ID."""
    try:
        alarm_service.delete_alarm(alarm_id, token_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
