from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.users.models import UserModel
from backend.src.app.src.services.users.repository import (
    UserRepository,
    inject_user_repository,
)
from backend.src.app.src.shared.database.engine import open_session


class UserService:
    def __init__(self, session: Session, user_repository: UserRepository):
        self._session = session
        self._user_repository = user_repository

    def get_or_create_user_from_oidc(self, oidc_user_info: dict) -> UserModel:
        """
        Retrieves a user from the database based on OIDC user information.
        If the user does not exist, it creates a new user.
        """
        user = self._user_repository.find_by_provider_sub(
            oidc_user_info["sub"]
        )

        if not user:
            # User does not exist, create a new one
            user = self._user_repository.create_from_oidc(oidc_user_info)
            self._session.commit()

        return user


def inject_user_service(
    session: Session = Depends(open_session),
    user_repository: UserRepository = Depends(inject_user_repository),
) -> UserService:
    return UserService(session, user_repository)
