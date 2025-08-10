from fastapi import Depends
from sqlalchemy.orm import Session

from ..auth.schemas import TokenData
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
        self, token_data: TokenData
    ) -> UserModel:
        """
        Looks for a user in the database by their Keycloak ID.
        If the user does not exist, it creates a new user profile with the data provided in the token.
        """
        user = self._user_repository.find_by_keycloak_id(token_data.id)

        if user:
            return user
        else:
            # creates a new user profile with the data provided in the token
            new_user_data = {
                "keycloak_id": token_data.id,
                "username": token_data.username,
                "email": token_data.email,
                "name": token_data.name,
            }

            # filter out None values to avoid inserting them into the database
            new_user_data_filtered = {
                k: v for k, v in new_user_data.items() if v is not None
            }

            user = self._user_repository.create_user(new_user_data_filtered)
            self._session.commit()
            return user


def inject_user_service(
    session: Session = Depends(open_session),
    user_repository: UserRepository = Depends(inject_user_repository),
) -> UserService:
    return UserService(session, user_repository)
