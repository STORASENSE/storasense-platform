from uuid import UUID
from typing import List

from fastapi import Depends, APIRouter, status, HTTPException, Query

from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.service import auth_service
from backend.src.app.src.shared.logger import get_logger
from backend.src.app.src.services.analytics.service import (
    AnalyticsService,
    inject_analytics_service,
)
from backend.src.app.src.services.analytics.schemas import (
    Window,
    SummaryItem,
)

router = APIRouter(tags=["Analytics"])
_logger = get_logger(__name__)


@router.get(
    "/analytics/byStorageId/{storage_id}",
    response_model=List[SummaryItem],
    status_code=status.HTTP_200_OK,
    description="Get analytics summary by storage ID",
)
def analytics_summary_by_storage_id(
    storage_id: UUID,
    window: Window = Query("7d"),
    analytics_service: AnalyticsService = Depends(inject_analytics_service),
    token_data: TokenData = Depends(auth_service.get_current_user),
):
    try:
        return analytics_service.summary_by_storage(
            storage_id, window, token_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
