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

    def find_by_username(self, username: str) -> Optional[UserModel]:
        query = select(UserModel).where(UserModel.username == username)
        return self.session.scalars(query).one_or_none()

    def create_user(
        self, username: str, password_hash: str, password_salt: str
    ) -> UserModel:
        user = UserModel()
        user.username = username
        user.password_hash = password_hash
        user.password_salt = password_salt

        self.session.add(user)
        self.session.flush()
        return user


def inject_user_repository(
    session: Session = Depends(open_session),
) -> UserRepository:
    return UserRepository(session)
