from datetime import datetime
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.src.app.src.services.auth.errors import (
    UnknownAuthPrincipalError,
    AuthorizationError,
)
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.shared.database.enums import UserRole
from backend.src.app.src.shared.logger import get_logger
from backend.src.app.src.services.measurements.models import MeasurementModel
from backend.src.app.src.services.users.repository import (
    UserRepository,
    inject_user_repository,
)
from backend.src.app.src.services.measurements.repository import (
    MeasurementRepository,
    inject_measurement_repository,
)
from backend.src.app.src.services.measurements.schemas import (
    CreateMeasurementRequest,
)
from backend.src.app.src.services.sensors.errors import SensorDoesNotExistError
from backend.src.app.src.services.sensors.repository import (
    SensorRepository,
    inject_sensor_repository,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.pagination import Page, PageRequest


_logger = get_logger(__name__)


class MeasurementService:
    def __init__(
        self,
        session: Session,
        measurement_repository: MeasurementRepository,
        sensor_repository: SensorRepository,
        user_repository: UserRepository,
    ):
        self._session = session
        self._measurement_repository = measurement_repository
        self._sensor_repository = sensor_repository
        self._user_repository = user_repository

    def find_all_by_sensor_id(
        self, sensor_id: UUID, page_request: PageRequest, token_data: TokenData
    ) -> Page[MeasurementModel]:
        """
        Finds all measurements that were recorded by the given sensor. The results are
        ordered from newest to oldest and are stored in a page.

        :param sensor_id: The ID of the sensor whose measurements should be retrieved.
        :param page_request: The pagination request.
        :param token_data: The token data of the requesting user.
        :return: The requested measurements.
        """
        # Check if sensor with the given ID exists
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if not sensor:
            raise SensorDoesNotExistError(
                f"Sensor with ID {sensor_id} doesnt exist."
            )

        # Validate user and their role in the storage (must be admin)
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        role = self._user_repository.find_user_role(user.id, sensor.storage_id)
        if role not in [UserRole.ADMIN, UserRole.CONTRIBUTOR]:
            raise AuthorizationError(
                "User is not authorized, to view measurements of this sensor."
            )

        return self._measurement_repository.find_all_by_sensor_id(
            sensor_id, page_request
        )

    def find_all_by_sensor_id_and_max_date(
        self, sensor_id: UUID, max_date: datetime, token_data: TokenData
    ) -> list[MeasurementModel]:
        """
        Finds all measurements that were recorded by the given sensor after the given date.
        The results are ordered from newest to oldest.
        Condition: The sensor with the given ID must exist.
        Condition_2: The user must be an admin or contributor of the storage the sensor belongs to.

        :param sensor_id: The ID of the sensor whose measurements should be retrieved.
        :param max_date: The date after which measurements should be retrieved.
        :param token_data: The token data of the requesting user.
        :return: The requested measurements.
        """
        _logger.info(
            f"Finding measurements for sensor '{sensor_id}' after date '{max_date}'"
        )

        # Check if sensor with the given ID exists
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if not sensor:
            _logger.info(f"Requested sensor '{sensor_id}' does not exist!")
            raise SensorDoesNotExistError(
                f"Sensor with ID '{sensor_id}' does not exist"
            )

        # Validate user and their role in the storage (must be admin)
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        role = self._user_repository.find_user_role(user.id, sensor.storage_id)
        if role not in [UserRole.ADMIN, UserRole.CONTRIBUTOR]:
            raise AuthorizationError(
                "User is not authorized, to view measurements of this sensor."
            )

        result = (
            self._measurement_repository.find_all_by_sensor_id_and_max_date(
                sensor_id, max_date
            )
        )
        _logger.info(f"Found {len(result)} measurements")
        return result

    def create_measurement(
        self, sensor_id: UUID, request: CreateMeasurementRequest, username: str
    ):
        """
        Creates a new measurement.
        Condition: The sensor with the given ID must exist and the requester must be "mqtt-client" (just Keycloak hard defined technical users named 'mqtt-client' are allowed to create measurements!).

        :param sensor_id: The ID of the sensor that recorded the measurement.
        :param request: The request for measurement creation.
        :param username: The username of the requester, must be "mqtt-client".
        :return: None
        """
        if (
            username != "service-account-mqtt-client"
        ):  # username of technical users is always theirs client_id
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Just MQTT-Clients are allowed to create measurements.",
            )

        sensor = self._sensor_repository.find_by_id(sensor_id)
        if not sensor:
            raise SensorDoesNotExistError(
                f"Sensor with ID {sensor_id} does not exist."
            )

        measurement = MeasurementModel()
        measurement.sensor_id = sensor_id
        measurement.value = request.value
        measurement.unit = request.unit
        measurement.created_at = request.created_at

        self._measurement_repository.create(measurement)
        self._session.commit()


def inject_measurement_service(
    session: Session = Depends(open_session),
    measurement_repository: MeasurementRepository = Depends(
        inject_measurement_repository
    ),
    sensor_repository: SensorRepository = Depends(inject_sensor_repository),
    user_repository: UserRepository = Depends(inject_user_repository),
) -> MeasurementService:
    return MeasurementService(
        session,
        measurement_repository,
        sensor_repository,
        user_repository,
    )
