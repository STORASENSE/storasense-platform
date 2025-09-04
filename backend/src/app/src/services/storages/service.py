from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
    UnknownAuthPrincipalError,
)
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.storages.errors import (
    StorageAlreadyExistsError,
    StorageNotFoundError,
)
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.services.storages.repository import (
    StorageRepository,
    inject_storage_repository,
)
from backend.src.app.src.services.user_storage_access.models import (
    UserStorageAccessModel,
)
from backend.src.app.src.services.user_storage_access.repository import (
    UserStorageAccessRepository,
    inject_user_storage_access_repository,
)
from backend.src.app.src.services.users.repository import (
    UserRepository,
    inject_user_repository,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.enums import UserRole


class StorageService:
    def __init__(
        self,
        session: Session,
        storage_repository: StorageRepository,
        user_repository: UserRepository,
        user_storage_access_repository: UserStorageAccessRepository,
    ):
        self.session = session
        self.storage_repository = storage_repository
        self.user_repository = user_repository
        self.user_storage_access_repository = user_storage_access_repository

    def find_storages_by_user_id(
        self, user_id: UUID, token_data: TokenData
    ) -> list[StorageModel]:
        """
        Find all storages that belong to a specific user.
        Condition: The user must be either an admin or a contributor of the storage.

        :param user_id: The ID of the user whose storages are to be retrieved.
        :return: A list of StorageModel instances associated with the user.
        """
        user = self.user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        return self.storage_repository.find_all_by_user_id(user_id)

    def find_my_storages(self, token_data: TokenData) -> list[StorageModel]:
        """
        Find all storages that belong to the authenticated user.
        Condition: The user must be either an admin or a contributor of the storage.

        :param token_data: The token data of the authenticated user.
        :return: A list of StorageModel instances associated with the authenticated user.
        """
        user = self.user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        return self.storage_repository.find_all_by_user_id(user.id)

    def create_storage(self, storage: StorageModel, token_data: TokenData):
        """
        Creates a storage and associates it with the user as an admin.

        :param storage: The storage to be created.
        :param token_data: The token data of the authenticated user.
        :return: None
        """
        user = self.user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        if storage.id is not None and self.storage_repository.exists(
            storage.id
        ):
            raise StorageAlreadyExistsError(
                "Could not create storage because a storage with the given ID already exists"
            )
        storage.user_associations.append(
            UserStorageAccessModel(user=user, role=UserRole.ADMIN)
        )
        self.storage_repository.create(storage)
        self.session.commit()

    def delete_storage(self, storage_id: UUID, token_data: TokenData):
        """
        Deletes a storage and associates it with the user as an admin.
        Condition: Only an admin of the storage can delete it.

        :param storage_id: The ID of the storage to be deleted.
        :param token_data: The token data of the authenticated user.
        :return: None
        """
        user = self.user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        storage = self.storage_repository.find_by_id(storage_id)
        if storage is None:
            raise StorageNotFoundError(
                "Could not delete storage because it does not exist"
            )
        role = self.user_storage_access_repository.find_user_role(
            user.id, storage.id
        )
        if role != UserRole.ADMIN:
            raise AuthorizationError(
                "Could not delete storage because requesting user does not have admin rights"
            )
        self.storage_repository.delete(storage)
        self.session.commit()


def inject_storage_service(
    session: Session = Depends(open_session),
    storage_repository: StorageRepository = Depends(inject_storage_repository),
    user_repository: UserRepository = Depends(inject_user_repository),
    user_storage_access_repository: UserStorageAccessRepository = Depends(
        inject_user_storage_access_repository
    ),
) -> StorageService:
    return StorageService(
        session,
        storage_repository,
        user_repository,
        user_storage_access_repository,
    )
