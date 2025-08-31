from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.src.app.src.services.users.models import UserModel
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.enums import UserRole
from backend.src.app.src.shared.database.join_tables.user_storage import (
    UserStorageAccess,
)
from backend.src.app.src.shared.repositories.base_repository import (
    BaseRepository,
)


class UserRepository(BaseRepository[UserModel, UUID]):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_id(self, object_id: UUID) -> Optional[UserModel]:
        """Finds a user by their ID."""
        query = select(UserModel).where(UserModel.id == object_id)
        return self.session.scalars(query).one_or_none()

    def find_by_keycloak_id(self, keycloak_id: str) -> Optional[UserModel]:
        """Finds a user by their ID ('sub'-Claim of JWT)."""
        query = select(UserModel).where(UserModel.keycloak_id == keycloak_id)
        return self.session.scalars(
            query
        ).one_or_none()  # returns a single UserModel or None

    def find_all_by_storage_id(self, storage_id: UUID) -> list[UserModel]:
        return (
            self.session.query(UserModel)
            .join(UserModel.accessed_storages)
            .filter_by(id=storage_id)
            .all()
        )

    def find_user_role(
        self, user_id: UUID, storage_id: UUID
    ) -> Optional[UserRole]:
        association = (
            self.session.query(UserStorageAccess)
            .where(UserStorageAccess.user_id == user_id)
            .where(UserStorageAccess.storage_id == storage_id)
            .one_or_none()
        )
        if association is None:
            return None
        return association.role

    def find_admin_by_storage_id(
        self, storage_id: UUID
    ) -> Optional[UserModel]:
        return (
            self.session.query(UserModel)
            .join(UserStorageAccess, UserModel.id == UserStorageAccess.user_id)
            .filter(
                UserStorageAccess.storage_id == storage_id,
                UserStorageAccess.role == UserRole.ADMIN,
            )
            .one_or_none()
        )

    def create_user(self, user_data: dict) -> UserModel:
        """
        Creates a new user in the database - based on the provided Keycloak user data.
        """
        new_user = UserModel(**user_data)
        self.session.add(new_user)
        return new_user


def inject_user_repository(
    session: Session = Depends(open_session),
) -> UserRepository:
    return UserRepository(session)
