from typing import Sequence
from uuid import UUID

from fastapi import Depends

from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.services.storages.repository import (
    StorageRepository,
    inject_storage_repository,
)


class StorageService:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    def find_storages_by_user_id(
        self, user_id: UUID
    ) -> Sequence[StorageModel]:
        return self.storage_repository.find_all_by_user_id(user_id)


def inject_storage_service(
    storage_repository: StorageRepository = Depends(inject_storage_repository),
) -> StorageService:
    return StorageService(storage_repository)
