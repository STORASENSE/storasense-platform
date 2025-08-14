from uuid import UUID

from fastapi import APIRouter, Depends

from backend.src.app.src.services.storages.schemas import StorageResponse
from backend.src.app.src.services.storages.service import (
    StorageService,
    inject_storage_service,
)

router = APIRouter(prefix="/storages", tags=["Storages"])


@router.get("/byUserId/{user_id}")
def storages_by_user_id(
    user_id: UUID,
    storage_service: StorageService = Depends(inject_storage_service),
) -> list[StorageResponse]:
    storages = storage_service.find_storages_by_user_id(user_id)
    return [
        StorageResponse(id=storage.id, name=storage.name)
        for storage in storages
    ]
