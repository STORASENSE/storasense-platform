from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.pagination import (
    PageRequest,
    Page,
    paginate,
)
from backend.src.app.src.shared.repositories.base_repository import (
    BaseRepository,
)


class StorageRepository(BaseRepository[StorageModel, UUID]):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_id(self, object_id: UUID) -> Optional[StorageModel]:
        return self.session.query(StorageModel).get(object_id)

    def find_all(self, page_request: PageRequest) -> Page[StorageModel]:
        return paginate(self.session.query(StorageModel), page_request)

    def find_by_name(self, name: str) -> Optional[StorageModel]:
        return (
            self.session.query(StorageModel)
            .where(StorageModel.name == name)
            .one_or_none()
        )

    def find_all_by_user_id(self, user_id: UUID) -> list[StorageModel]:
        return (
            self.session.query(StorageModel)
            .join(StorageModel.accessing_users)
            .filter_by(id=user_id)
            .all()
        )

    def exists_by_name(self, name: str) -> bool:
        return self.find_by_name(name) is not None


def inject_storage_repository(session: Session = Depends(open_session)):
    return StorageRepository(session)
