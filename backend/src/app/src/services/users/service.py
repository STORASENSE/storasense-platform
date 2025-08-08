# backend/src/app/src/services/users/service.py

from fastapi import Depends
from sqlalchemy.orm import Session

from .models import UserModel
from .repository import (
    UserRepository,
    inject_user_repository,
)
from ...shared.database.engine import open_session


class UserService:
    def __init__(self, session: Session, user_repository: UserRepository):
        self._session = session
        self._user_repository = user_repository

    def get_or_create_user_by_keycloak_id(
        self, keycloak_id: str, username: str
    ) -> UserModel:
        user = self._user_repository.find_by_keycloak_id(keycloak_id)

        if user:
            return user
        else:
            new_user_data = {
                "keycloak_id": keycloak_id,
                "username": username,
            }
            user = self._user_repository.create_user(new_user_data)
            self._session.commit()
            return user


def inject_user_service(
    session: Session = Depends(open_session),
    user_repository: UserRepository = Depends(inject_user_repository),
) -> UserService:
    return UserService(session, user_repository)
