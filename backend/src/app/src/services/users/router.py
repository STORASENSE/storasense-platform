from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException

from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
    UnknownAuthPrincipalError,
)
from ..auth.service import auth_service, TokenData
from ..users.service import UserService, inject_user_service
from .models import UserModel
from .schemas import UserPublicResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me", response_model=UserPublicResponse, status_code=status.HTTP_200_OK
)
async def read_users_me(
    token_data: TokenData = Depends(auth_service.get_current_user),
    user_service: UserService = Depends(inject_user_service),
):
    try:
        db_user: UserModel = user_service.get_or_create_user_by_keycloak_id(
            token_data=token_data
        )
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Authenticated user not found.",
            )

        return UserPublicResponse(
            username=db_user.username,
            email=db_user.email,
            name=db_user.name,
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


@router.get("/byStorageId/{storage_id}")
async def find_users_by_storage_id(
    storage_id: UUID,
    token_data: TokenData = Depends(auth_service.get_current_user),
    user_service: UserService = Depends(inject_user_service),
) -> list[UserPublicResponse]:
    try:
        users = user_service.find_all_by_storage_id(storage_id, token_data)
    except (UnknownAuthPrincipalError, AuthorizationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication principal is not authorized to access the requested resource.",
        )
    return [
        UserPublicResponse(
            username=user.username,
            email=user.email,
            name=user.name,
        )
        for user in users
    ]
