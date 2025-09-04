from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.src.app.src.services.users.models import UserModel
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.base_repository import (
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

    def find_by_username(self, username: str) -> Optional[UserModel]:
        return (
            self.session.query(UserModel)
            .where(UserModel.username == username)
            .one_or_none()
        )

    def find_all_by_storage_id(self, storage_id: UUID) -> list[UserModel]:
        return (
            self.session.query(UserModel)
            .join(UserModel.accessed_storages)
            .filter_by(id=storage_id)
            .all()
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
