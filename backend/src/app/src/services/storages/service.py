from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.auth.errors import UnknownAuthPrincipalError
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.storages.errors import (
    StorageAlreadyExistsError,
)
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.services.storages.repository import (
    StorageRepository,
    inject_storage_repository,
)
from backend.src.app.src.services.users.repository import (
    UserRepository,
    inject_user_repository,
)
from backend.src.app.src.shared.database.engine import open_session


class StorageService:
    def __init__(
        self,
        session: Session,
        storage_repository: StorageRepository,
        user_repository: UserRepository,
    ):
        self.session = session
        self.storage_repository = storage_repository
        self.user_repository = user_repository

    def find_storages_by_user_id(self, user_id: UUID) -> list[StorageModel]:
        return self.storage_repository.find_all_by_user_id(user_id)

    def find_my_storages(self, token_data: TokenData) -> list[StorageModel]:
        user = self.user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        return self.storage_repository.find_all_by_user_id(user.id)

    def create_storage(self, storage: StorageModel, token_data: TokenData):
        user = self.user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        if storage.name is None:
            raise ValueError(
                "Could not create storage because given storage name was None"
            )
        if storage.id is not None and self.storage_repository.exists(
            storage.id
        ):
            raise StorageAlreadyExistsError(
                "Could not create storage because a storage with the given ID already exists"
            )
        if self.storage_repository.exists_by_name(storage.name):
            raise StorageAlreadyExistsError(
                "Could not create storage because a storage with the given name already exists"
            )
        storage.accessing_users.append(user)
        self.storage_repository.create(storage)
        self.session.commit()


def inject_storage_service(
    session: Session = Depends(open_session),
    storage_repository: StorageRepository = Depends(inject_storage_repository),
    user_repository: UserRepository = Depends(inject_user_repository),
) -> StorageService:
    return StorageService(session, storage_repository, user_repository)
