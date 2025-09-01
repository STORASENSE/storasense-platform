import json
import os
from datetime import datetime, timezone, timedelta
from uuid import UUID

from confluent_kafka import Producer

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
    UnknownAuthPrincipalError,
)
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.measurements.repository import (
    MeasurementRepository,
    inject_measurement_repository,
)
from backend.src.app.src.services.sensors.repository import (
    SensorRepository,
    inject_sensor_repository,
)
from backend.src.app.src.services.storages.repository import (
    StorageRepository,
    inject_storage_repository,
)
from backend.src.app.src.services.users.repository import (
    UserRepository,
    inject_user_repository,
)
from backend.src.app.src.services.user_storage_access.repository import (
    UserStorageAccessRepository,
    inject_user_storage_access_repository,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.enums import UserRole


class SensorService:
    def __init__(
        self,
        session: Session,
        sensor_repository: SensorRepository,
        storage_repository: StorageRepository,
        measurement_repository: MeasurementRepository,
        user_storage_access_repository: UserStorageAccessRepository,
        user_repository: UserRepository,
    ):
        self._measurement_repository = measurement_repository
        self._session = session
        self._sensor_repository = sensor_repository
        self._storage_repository = storage_repository
        self._user_storage_access_repository = user_storage_access_repository
        self._user_repository = user_repository

    def check_sensor_status(
        self, sensor_id: UUID, max_age_minutes: int, token_data: TokenData
    ) -> dict:
        """
        Checks if a sensor is online based on the age of its last measurement.
        A sensor is considered online if its last measurement is within the specified max_age_minutes.
        Condition: The sensor with the given ID must not exist.
        Condition_2: The user must be part of the storage.

        :param max_age_minutes: The maximum age in minutes for a sensor to be considered online.
        :param sensor_id: The ID of the sensor to check.
        :param token_data: The token data of the requesting user.
        :return: A dictionary containing the sensor ID, online status, last measurement value, and last measurement time. The last 2 are always returned, but can be None.
        """
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )

        sensor = self._sensor_repository.find_by_id(sensor_id)
        if sensor is None:
            raise ValueError(f"Sensor with ID {sensor_id} doesnt exist.")

        role = self._user_storage_access_repository.find_user_role(
            user.id, sensor.storage_id
        )
        if role not in (UserRole.ADMIN, UserRole.CONTRIBUTOR):
            raise AuthorizationError(
                "Could not return sensor status because requesting user is not part of the storage"
            )

        # Check if sensor with the given ID exists
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if sensor is None:
            raise ValueError(f"Sensor with ID {sensor_id} doesnt exist.")

        # Get always the latest measurement
        last_measurement = (
            self._measurement_repository.find_latest_by_sensor_id(sensor_id)
        )

        last_value = last_measurement.value if last_measurement else None
        last_time = last_measurement.timestamp if last_measurement else None

        # Set is_online based on the age of the last measurement (is it within max_age_minutes?)
        is_online = False
        if last_measurement and last_time:
            if last_time.tzinfo is None:
                last_time = last_time.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            time_threshold = now - timedelta(minutes=max_age_minutes)
            is_online = last_time >= time_threshold

        return {
            "sensor_id": str(sensor_id),
            "is_online": is_online,
            "last_measurement": last_value,
            "last_measurement_time": last_time,
        }

    def find_sensor_by_id(
        self, sensor_id: UUID, token_data: TokenData
    ) -> SensorModel:
        """
        Finds a sensor by its ID.
        Condition: The sensor with the given ID must not exist.
        Condition_2: The user must be part of the storage.

        :param sensor_id: The ID of the sensor to find.
        :param token_data: The token data of the requesting user.
        :return: The sensor with the given ID.
        """
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )

        sensor = self._sensor_repository.find_by_id(sensor_id)
        if sensor is None:
            raise ValueError(f"Sensor with ID {sensor_id} doesnt exist.")

        role = self._user_storage_access_repository.find_user_role(
            user.id, sensor.storage_id
        )
        if role not in (UserRole.ADMIN, UserRole.CONTRIBUTOR):
            raise AuthorizationError(
                "Could not return sensor because requesting user is not part of the storage"
            )

        # Check if sensor with the given ID exists
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if sensor is None:
            raise ValueError(f"Sensor with ID {sensor_id} doesnt exist.")

        return self._sensor_repository.find_by_id(sensor_id)

    def find_sensors_by_storage_id(
        self, storage_id: UUID, token_data: TokenData
    ) -> list[SensorModel]:
        """
        Finds all sensors by the storage ID.
        Condition: The storage with the given ID must exist.
        Condition_2: The user must be part of the storage.

        :param storage_id: The ID of the storage to find sensors for.
        :param token_data: The token data of the requesting user.
        :return: A list of sensors belonging to the specified storage.
        """
        storage = self._storage_repository.find_by_id(storage_id)
        if not storage:
            raise ValueError(f"Storage with ID {storage} does not exist.")

        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )

        role = self._user_storage_access_repository.find_user_role(
            user.id, storage_id
        )
        if role not in (UserRole.ADMIN, UserRole.CONTRIBUTOR):
            raise AuthorizationError(
                "Could not return sensors because requesting user is not part of the storage"
            )

        return self._sensor_repository.find_all_by_storage_id(storage_id)

    def create_sensor(self, sensor_id: UUID, token_data: TokenData, request):
        """
        Creates a new sensor by its ID and sends min/max allowed values to Kafka topic 'sensor_values' (alarm system).
        Condition: The sensor with the given ID must not exist.
        Condition_2: The storage with the given ID must exist.
        Condition_3: The user must have admin rights in the storage.

        :param sensor_id: The ID of the sensor to be created.
        :param request: The request for sensor creation.
        :param token_data: The ID of the user creating the sensor.
        """
        # Validate user and their role in the storage (must be admin)
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        role = self._user_storage_access_repository.find_user_role(
            user.id, request.storage_id
        )
        if role != UserRole.ADMIN:
            raise AuthorizationError(
                "Could not create sensor because requesting user does not have admin rights"
            )
        # Check if sensor with the given ID already exists
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if sensor:
            raise ValueError(f"Sensor with ID {sensor_id} already exists.")

        # Check if storage with the given ID exists
        storage = self._storage_repository.find_by_id(request.storage_id)
        if not storage:
            raise ValueError(f"Storage with ID {sensor_id} does not exist.")

        sensor = SensorModel()
        sensor.id = sensor_id
        sensor.type = request.type
        sensor.storage_id = request.storage_id
        sensor.name = request.name
        sensor.allowed_min = request.allowed_min
        sensor.allowed_max = request.allowed_max

        # Kafka Producer to send sensor data to the 'sensor_values' topic when a new sensor is created
        KAFKA_HOST = os.getenv("KAFKA_HOST")
        producer = Producer(
            {
                "bootstrap.servers": KAFKA_HOST,
                "partitioner": "murmur2",
            }  # murmur2 for compatibility with Java clients
        )
        sensorID = str(sensor.id)
        sensor_data = {
            "sensorId": sensorID,
            "allowedMin": sensor.allowed_min,
            "allowedMax": sensor.allowed_max,
            "email": user.email,  # email for alarm-system notifications
        }

        # Important: Commit only after Kafka message is sent successfully and database operation is successful
        try:
            self._sensor_repository.create(sensor)
            producer.produce(
                "sensor_values",
                key=sensorID.encode("utf-8"),
                value=json.dumps(sensor_data).encode("utf-8"),
            )
            producer.flush()
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise RuntimeError("Failed to create sensor")

    def delete_sensor(self, sensor_id: UUID, token_data: TokenData, request):
        """
        Deletes a sensor by its ID.
        Condition: The sensor with the given ID must exist.
        Condition_2: The user must have admin rights in the storage.

        :param sensor_id: The ID of the sensor to be deleted.
        :param request: The request for sensor deletion.
        :param token_data: The ID of the user deleting the sensor.
        """
        # Validate user and their role in the storage (must be admin)
        user = self._user_repository.find_by_keycloak_id(token_data.id)
        if user is None:
            raise UnknownAuthPrincipalError(
                "Requesting authentication principal does not exist"
            )
        role = self._user_storage_access_repository.find_user_role(
            user.id, request.storage_id
        )
        if role != UserRole.ADMIN:
            raise AuthorizationError(
                "Could not delete sensor because requesting user does not have admin rights"
            )
        # Check if sensor with the given ID exists
        sensor = self._sensor_repository.find_by_id(sensor_id)
        if not sensor:
            raise ValueError(f"Sensor with ID {sensor_id} does not exist.")

        self._sensor_repository.delete(sensor)
        self._session.commit()

    def push_all_sensors_to_kafka(self):
        """
        Pushes all sensors with their allowed min/max values to the Kafka topic 'sensor_values'.
        Only used when system is started after shutdown to initialize the alarm system with all sensors.
        """
        KAFKA_HOST = os.getenv("KAFKA_HOST")
        producer = Producer(
            {"bootstrap.servers": KAFKA_HOST, "partitioner": "murmur2"}
        )
        sensors = self._sensor_repository.find_all_unpaginated()
        if not sensors:
            return  # No sensors to push
        for sensor in sensors:
            # Admin-User for the storage the sensor belongs to (to get the admins email for notifications)
            admin_user = (
                self._user_storage_access_repository.find_admin_by_storage_id(
                    sensor.storage_id
                )
            )
            email = admin_user.email if admin_user else None
            sensor_data = {
                "sensorId": str(sensor.id),
                "allowedMin": sensor.allowed_min,
                "allowedMax": sensor.allowed_max,
                "email": email,
            }
            producer.produce(
                "sensor_values",
                key=str(sensor.id).encode("utf-8"),
                value=json.dumps(sensor_data).encode("utf-8"),
            )
        producer.flush()


def inject_sensor_service(
    session: Session = Depends(open_session),
    sensor_repository: SensorRepository = Depends(inject_sensor_repository),
    storage_repository: StorageRepository = Depends(inject_storage_repository),
    measurement_repository: MeasurementRepository = Depends(
        inject_measurement_repository
    ),
    user_storage_access_repository: UserStorageAccessRepository = Depends(
        inject_user_storage_access_repository
    ),
    user_repository: UserRepository = Depends(inject_user_repository),
) -> SensorService:
    return SensorService(
        session,
        sensor_repository,
        storage_repository,
        measurement_repository,
        user_storage_access_repository,
        user_repository,
    )
