from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Sequence
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

    def find_all(self, page_request: [PageRequest]) -> Page[StorageModel]:
        return paginate(self.session.query(StorageModel), page_request)

    def find_all_by_user_id(self, user_id: UUID) -> Sequence[StorageModel]:
        return (
            self.session.query(StorageModel)
            .join(StorageModel.accessing_users)
            .filter_by(id=user_id)
            .all()
        )


def inject_storage_repository(session: Session = Depends(open_session)):
    return StorageRepository(session)
