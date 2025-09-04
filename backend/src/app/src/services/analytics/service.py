from __future__ import annotations
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends

from backend.src.app.src.services.analytics.repository import (
    AnalyticsRepository,
)
from backend.src.app.src.services.auth.errors import (
    UnknownAuthPrincipalError,
    AuthorizationError,
)
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.user_storage_access.repository import (
    inject_user_storage_access_repository,
    UserStorageAccessRepository,
)
from backend.src.app.src.services.users.repository import (
    inject_user_repository,
    UserRepository,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.enums import UserRole

WINDOW_TO_INTERVAL = {"7d": "7 days", "30d": "30 days", "365d": "365 days"}


class AnalyticsService:
    def __init__(
        self,
        session: Session,
        repo: AnalyticsRepository,
        user_repository: UserRepository,
        user_storage_access_repository: UserStorageAccessRepository,
    ):
        self._session = session
        self._repo = repo
        self.user_repository = user_repository
        self.user_storage_access_repository = user_storage_access_repository

    def summary_by_storage(
        self, storage_id: UUID, window: str, token_data: TokenData
    ):
        """
        Get sensor summary by storage.

        :param storage_id: Storage ID for which to get the summary
        :param window: Time window (e.g., '7d', '30d', '365d')
        :param token_data: Auth token data of the requesting user
        :return: Sensor summary data
        """
        user = self.user_repository.find_by_keycloak_id(token_data.id)

        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        role = self.user_storage_access_repository.find_user_role(
            user.id, storage_id
        )
        if role not in (UserRole.ADMIN, UserRole.CONTRIBUTOR):
            raise AuthorizationError(
                "User is not authorized to access analytics for this storage"
            )
        interval = WINDOW_TO_INTERVAL[window]
        return self._repo.get_sensor_summary_by_storage(storage_id, interval)


def inject_analytics_service(
    session: Session = Depends(open_session),
    user_repository: UserRepository = Depends(inject_user_repository),
    user_storage_access_repository: UserStorageAccessRepository = Depends(
        inject_user_storage_access_repository
    ),
) -> AnalyticsService:
    repo = AnalyticsRepository(session)
    return AnalyticsService(
        session, repo, user_repository, user_storage_access_repository
    )
