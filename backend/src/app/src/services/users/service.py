from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
    UnknownAuthPrincipalError,
)
from backend.src.app.src.services.storages.errors import StorageNotFoundError
from backend.src.app.src.services.storages.repository import (
    StorageRepository,
    inject_storage_repository,
)
from backend.src.app.src.services.user_storage_access.repository import (
    UserStorageAccessRepository,
    inject_user_storage_access_repository,
)
from backend.src.app.src.services.users.errors import UserDoesNotExistError
from backend.src.app.src.shared.database.enums import UserRole
from .schemas import UserByStorageIdResponse

from ..auth.schemas import TokenData
from .models import UserModel
from .repository import (
    UserRepository,
    inject_user_repository,
)
from ...shared.database.engine import open_session


def is_technical_user(token_data: TokenData) -> bool:
    if not token_data.email and not token_data.name:
        return True
    return False


class UserService:
    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
        storage_repository: StorageRepository,
        user_storage_access_repository: UserStorageAccessRepository,
    ):
        self._session = session
        self._user_repository = user_repository
        self._storage_repository = storage_repository
        self._user_storage_access_repository = user_storage_access_repository

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
            role = self._user_storage_access_repository.find_user_role(
                user.id, storage_id
            )
            if role is None:
                continue
            result.append(
                UserByStorageIdResponse(
                    id=user.id, username=user.username, role=role
                )
            )
        return result

    def _raise_error_if_not_admin(
        self, storage_id: UUID, token_data: TokenData
    ):
        principal = self._user_repository.find_by_keycloak_id(token_data.id)
        if principal is None:
            raise UnknownAuthPrincipalError(
                "Could not commit to storage because authentication token is invalid"
            )
        principal_role = self._user_storage_access_repository.find_user_role(
            principal.id, storage_id
        )
        if not principal_role == UserRole.ADMIN:
            raise AuthorizationError(
                "Could not commit to storage because authentication principal is not admin of storage"
            )

    def add_user_to_storage(
        self, username: str, storage_id: UUID, token_data: TokenData
    ):
        self._raise_error_if_not_admin(storage_id, token_data)
        user = self._user_repository.find_by_username(username)
        if user is None:
            raise UserDoesNotExistError(
                "Could not add user to storage because user does not exist"
            )
        if not self._storage_repository.exists(storage_id):
            raise StorageNotFoundError(
                "Could not add user to storage because storage does not exist"
            )
        self._user_storage_access_repository.add_user_to_storage(
            user.id, storage_id, UserRole.CONTRIBUTOR
        )
        self._session.commit()

    def remove_user_from_storage(
        self, username: str, storage_id: UUID, token_data: TokenData
    ):
        self._raise_error_if_not_admin(storage_id, token_data)
        user = self._user_repository.find_by_username(username)
        if user is None:
            raise UserDoesNotExistError(
                "Could not remove user from storage because user does not exist"
            )
        user_role = self._user_storage_access_repository.find_user_role(
            user.id, storage_id
        )
        if user_role == UserRole.ADMIN:
            raise AuthorizationError(
                "Could not remove user from storage because user is admin of storage"
            )
        if not self._storage_repository.exists(storage_id):
            raise StorageNotFoundError(
                "Could not remove user from storage because storage does not exist"
            )
        self._user_storage_access_repository.remove_user_from_storage(
            user.id, storage_id
        )
        self._session.commit()


def inject_user_service(
    session: Session = Depends(open_session),
    user_repository: UserRepository = Depends(inject_user_repository),
    storage_repository: StorageRepository = Depends(inject_storage_repository),
    user_storage_access_repository: UserStorageAccessRepository = Depends(
        inject_user_storage_access_repository
    ),
) -> UserService:
    return UserService(
        session,
        user_repository,
        storage_repository,
        user_storage_access_repository,
    )
