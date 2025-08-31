from uuid import UUID
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.alarms.models import AlarmModel
from backend.src.app.src.services.alarms.repository import (
    AlarmRepository,
    inject_alarm_repository,
)
from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
    UnknownAuthPrincipalError,
)
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.storages.repository import (
    StorageRepository,
    inject_storage_repository,
)
from backend.src.app.src.services.sensors.repository import (
    SensorRepository,
    inject_sensor_repository,
)
from backend.src.app.src.services.users.repository import (
    UserRepository,
    inject_user_repository,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.enums import UserRole
from backend.src.app.src.shared.database.pagination import PageRequest, Page


class AlarmService:
    def __init__(
        self,
        session: Session,
        alarm_repository: AlarmRepository,
        storage_repository: StorageRepository,
        sensor_repository: SensorRepository,
        user_repository: UserRepository,
    ):
        self._session = session
        self._alarm_repository = alarm_repository
        self._storage_repository = storage_repository
        self._sensor_repository = sensor_repository
        self._user_repository = user_repository

    def find_alarm_by_id(
        self, alarm_id: UUID, token_data: TokenData
    ) -> Optional[AlarmModel]:
        """
        Finds an alarm by its ID with validating if a user is part of the storage where the sensor is located.

        :param alarm_id: The ID of the alarm to find.
        :param token_data: The token data of the requesting user.
        :return: The found alarm or None if not found.
        """
        alarm = self._alarm_repository.find_by_id(alarm_id)
        if not alarm:
            raise ValueError(f"Alarm with ID {alarm_id} does not exist.")

        # Get the sensor to which the alarm is linked
        sensor = self._sensor_repository.find_by_id(alarm.sensor_id)

        # Validate user and their role in the storage where sensor is located (must be admin)
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        role = self._user_repository.find_user_role(user.id, sensor.storage_id)
        if role not in (UserRole.ADMIN, UserRole.CONTRIBUTOR):
            raise AuthorizationError(
                "Could not delete alarm because requesting user is not part of the storage"
            )

        return alarm

    def delete_alarm(self, alarm_id: UUID, token_data: TokenData) -> None:
        """
        Deletes an alarm by its ID after validating user permissions.

        :param alarm_id: The ID of the alarm to delete.
        :param token_data: The token data of the requesting user.
        :return: None
        """

        # Verify alarm exists
        alarm = self._alarm_repository.find_by_id(alarm_id)
        if not alarm:
            raise ValueError(f"Alarm with ID {alarm_id} does not exist.")

        # Get the sensor to which the alarm is linked
        sensor = self._sensor_repository.find_by_id(alarm.sensor_id)

        # Validate user and their role in the storage where sensor is located (must be admin)
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        role = self._user_repository.find_user_role(user.id, sensor.storage_id)
        if role != UserRole.ADMIN:
            raise AuthorizationError(
                "Could not delete alarm because requesting user does not have admin rights"
            )
        self._alarm_repository.delete(alarm)
        self._session.commit()

    def find_alarms_by_storage_id(
        self,
        storage_id: UUID,
        page_request: PageRequest,
        token_data: TokenData,
    ) -> Page[AlarmModel]:
        """
        Returns all alarms for a given storage (linked via Sensor → Measurements),
        sorted by alarm timestamp in descending order and paginated.
        Validates if the user is part of the storage before returning alarms.
        Note: For performance reasons, a raw SQL query is used.

        :param storage_id: The ID of the storage to get alarms for.
        :param page_request: The pagination request.
        :param token_data: The token data of the requesting user.
        :return: A page containing the requested alarm data.
        """
        # Verify storage exists first
        storage = self._storage_repository.find_by_id(storage_id)
        if not storage:
            raise ValueError(f"Storage with ID {storage_id} does not exist.")

        # Validate user and their role in the storage where sensor is located (must be admin)
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        role = self._user_repository.find_user_role(user.id, storage.id)
        if role not in (UserRole.ADMIN, UserRole.CONTRIBUTOR):
            raise AuthorizationError(
                "Could not return alarm(s) because requesting user is not part of the storage"
            )

        return self._alarm_repository.find_alarms_by_storage_id(
            storage_id, page_request
        )


def inject_alarm_service(
    session: Session = Depends(open_session),
    alarm_repository: AlarmRepository = Depends(inject_alarm_repository),
    storage_repository: StorageRepository = Depends(inject_storage_repository),
    sensor_repository: SensorRepository = Depends(inject_sensor_repository),
    user_repository: UserRepository = Depends(inject_user_repository),
) -> AlarmService:
    return AlarmService(
        session,
        alarm_repository,
        storage_repository,
        sensor_repository,
        user_repository,
    )
