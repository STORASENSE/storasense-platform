from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.src.app.src.services.users.models import UserModel
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.repositories.base_repository import (
    BaseRepository,
)


class UserRepository(BaseRepository[UserModel, UUID]):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_id(self, user_id: UUID) -> Optional[UserModel]:
        """Finds a user by their ID."""
        query = select(UserModel).where(UserModel.id == user_id)
        return self.session.scalars(query).one_or_none()

    def find_by_provider_sub(self, provider_sub: str) -> Optional[UserModel]:
        """Finds a user by their id from the OIDC provider."""
        query = select(UserModel).where(UserModel.provider_sub == provider_sub)
        return self.session.scalars(query).one_or_none()

    def find_by_email(self, email: str) -> Optional[UserModel]:
        """Finds a user by their email address."""
        query = select(UserModel).where(UserModel.email == email)
        return self.session.scalars(query).one_or_none()

    def create_from_oidc(self, oidc_user_info: dict) -> UserModel:
        """Creates a new user from OIDC user information."""
        user = UserModel()
        user.email = oidc_user_info.get("email")
        user.provider_sub = oidc_user_info.get("sub")
        user.name = oidc_user_info.get("name")
        user.role = "user"

        self.session.add(user)
        self.session.flush()  # Don't commit here => Service has to do that!
        return user


def inject_user_repository(
    session: Session = Depends(open_session),
) -> UserRepository:
    return UserRepository(session)
