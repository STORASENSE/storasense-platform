from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException

from backend.src.app.src.services.auth.errors import UnknownAuthPrincipalError
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.service import auth_service
from backend.src.app.src.services.storages.errors import (
    StorageAlreadyExistsError,
)
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.services.storages.schemas import (
    CreateStorageRequest,
    StorageResponse,
)
from backend.src.app.src.services.storages.service import (
    StorageService,
    inject_storage_service,
)

router = APIRouter(prefix="/storages", tags=["Storages"])


@router.get("/myStorages")
def get_my_storages(
    token_data: TokenData = Depends(auth_service.get_current_user),
    storage_service: StorageService = Depends(inject_storage_service),
) -> list[StorageResponse]:
    try:
        storages = storage_service.find_my_storages(token_data)
    except UnknownAuthPrincipalError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication principal is unauthorized to access the requested resource",
        )
    return [
        StorageResponse(id=storage.id, name=storage.name)
        for storage in storages
    ]


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


@router.post("")
def create_storage(
    request: CreateStorageRequest,
    token_data: TokenData = Depends(auth_service.get_current_user),
    storage_service: StorageService = Depends(inject_storage_service),
) -> None:
    storage = StorageModel(name=request.name)
    try:
        storage_service.create_storage(storage, token_data)
    except UnknownAuthPrincipalError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication principal is unauthorized to access the requested resource",
        )
    except StorageAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=repr(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e)
        )
