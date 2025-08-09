from fastapi import APIRouter, Depends, status, HTTPException
from ..auth.service import auth_service, TokenData
from ..users.service import UserService, inject_user_service
from .models import UserModel
from .schemas import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_users_me(
    token_data: TokenData = Depends(auth_service.get_current_user),
    user_service: UserService = Depends(inject_user_service),
):
    db_user: UserModel = user_service.get_or_create_user_by_keycloak_id(
        token_data=token_data
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authenticated user not found and couldn't be created.",
        )
    return db_user
