from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session
from backend.src.app.src.services.user_storage_access.models import (
    UserStorageAccessModel,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.enums import UserRole
from backend.src.app.src.shared.database.base_repository import BaseRepository


class UserStorageAccessRepository(
    BaseRepository[UserStorageAccessModel, tuple[UUID, UUID]]
):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_id(
        self, object_id: tuple[UUID, UUID]
    ) -> UserStorageAccessModel | None:
        user_id, storage_id = object_id
        return (
            self.session.query(UserStorageAccessModel)
            .where(UserStorageAccessModel.user_id == user_id)
            .where(UserStorageAccessModel.storage_id == storage_id)
            .one_or_none()
        )

    def find_user_role(
        self, user_id: UUID, storage_id: UUID
    ) -> UserRole | None:
        association = self.find_by_id((user_id, storage_id))
        if association is None:
            return None
        return association.role

    def add_user_to_storage(
        self, user_id: UUID, storage_id: UUID, role: UserRole
    ):
        if self.exists((user_id, storage_id)):
            return
        assoc = UserStorageAccessModel(
            user_id=user_id, storage_id=storage_id, role=role
        )
        self.create(assoc)


def inject_user_storage_access_repository(
    session: Session = Depends(open_session),
):
    return UserStorageAccessRepository(session)
