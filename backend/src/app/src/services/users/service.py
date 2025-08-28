from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
    UnknownAuthPrincipalError,
)
from .schemas import UserByStorageIdResponse

from ..auth.schemas import TokenData
from .models import UserModel
from .repository import (
    UserRepository,
    inject_user_repository,
)
from ...shared.database.engine import open_session
from ...shared.logger import get_logger


_logger = get_logger(__name__)


def is_technical_user(token_data: TokenData) -> bool:
    if not token_data.email and not token_data.name:
        return True
    return False


class UserService:
    def __init__(self, session: Session, user_repository: UserRepository):
        self._session = session
        self._user_repository = user_repository

    def get_or_create_user_by_keycloak_id(
        self, token_data: TokenData
    ) -> UserModel:
        """
        Looks for a user in the database by their Keycloak ID.
        If the user does not exist, it creates a new user profile with the data provided in the token.
        """
        user = self._user_repository.find_by_keycloak_id(token_data.id)

        if user:
            return user

        # Technical User Registration flow
        if is_technical_user(token_data):
            new_user_data = {
                "keycloak_id": token_data.id,
                "username": token_data.username,
                "email": None,
                "name": None,
            }
            # filter out None values to avoid inserting them into the database
            new_user_data_filtered = {
                k: v for k, v in new_user_data.items() if v is not None
            }

            user = self._user_repository.create_user(new_user_data_filtered)
            self._session.commit()
            return user

        else:
            # creates a new user profile with the data provided in the token
            new_user_data = {
                "keycloak_id": token_data.id,
                "username": token_data.username,
                "email": token_data.email,
                "name": token_data.name,
            }

            # filter out None values to avoid inserting them into the database
            new_user_data_filtered = {
                k: v for k, v in new_user_data.items() if v is not None
            }

            user = self._user_repository.create_user(new_user_data_filtered)
            self._session.commit()
            return user

    def find_all_by_storage_id(
        self, storage_id: UUID, token_data: TokenData
    ) -> list[UserByStorageIdResponse]:
        principal = self._user_repository.find_by_keycloak_id(token_data.id)
        if principal is None:
            raise UnknownAuthPrincipalError(
                "Could not fetch all users in storage because authentication token is invalid"
            )
        users = self._user_repository.find_all_by_storage_id(storage_id)
        if principal not in users:
            raise AuthorizationError(
                "Could not fetch all users in storage because requesting client is unauthorized"
            )
        result: list[UserByStorageIdResponse] = []
        for user in users:
            role = self._user_repository.find_user_role(user.id, storage_id)
            result.append(
                UserByStorageIdResponse(
                    id=user.id, username=user.username, role=role
                )
            )
        return result


def inject_user_service(
    session: Session = Depends(open_session),
    user_repository: UserRepository = Depends(inject_user_repository),
) -> UserService:
    return UserService(session, user_repository)
