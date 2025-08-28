import os
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from uuid import UUID

from backend.src.app.src.services.alarms.models import AlarmModel
from backend.src.app.src.services.users.models import UserModel
from backend.src.app.src.shared.database.join_tables.user_storage import (
    UserStorageAccess,
)
from backend.src.app.src.shared.logger import get_logger
from backend.src.app.src.services.measurements.models import MeasurementModel
from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.shared.database.enums import (
    SensorType,
    MeasurementUnit,
    AlarmSeverity,
    UserRole,
)


_logger = get_logger(__name__)


def seed_storages(session: Session):
    storages: list[StorageModel] = [
        StorageModel(
            id=UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"),
            name="MyStorage",
        )
    ]
    session.add_all(storages)
    session.flush()


def seed_sensors(session: Session):
    for storage in session.query(StorageModel).all():
        temp_inside = SensorModel(
            name="Temperature (Inside)",
            type=SensorType.TEMPERATURE_INSIDE,
            storage_id=storage.id,
            allowed_min=1.0,
            allowed_max=5.0,
        )
        temp_outside = SensorModel(
            name="Temperature (Outside)",
            type=SensorType.TEMPERATURE_OUTSIDE,
            storage_id=storage.id,
            allowed_min=10.0,
            allowed_max=30.0,
        )
        humidity = SensorModel(
            name="Humidity",
            type=SensorType.HUMIDITY,
            storage_id=storage.id,
            allowed_min=20.0,
            allowed_max=80.0,
        )
        ultrasonic = SensorModel(
            name="Ultrasonic",
            type=SensorType.ULTRASONIC,
            storage_id=storage.id,
            allowed_min=100.0,
            allowed_max=100.0,
        )
        air = SensorModel(
            name="Air Quality",
            type=SensorType.GAS,
            storage_id=storage.id,
            allowed_min=10.0,
            allowed_max=20.0,
        )
        session.add_all([temp_inside, temp_outside, humidity, ultrasonic, air])
        session.flush()


def seed_measurements(session: Session):
    for sensor in session.query(SensorModel).all():
        _logger.info(f"Generating measurements for sensor {sensor.name}")

        # Decides randomly wether 15 measurements should be under the allowed minimum or above the allowed maximum
        outlier_type = random.choice(["min", "max"])
        outlier_value = (
            sensor.allowed_min - 0.1
            if outlier_type == "min"
            else sensor.allowed_max + 0.1
        )

        measurements: list[MeasurementModel] = []

        for i in range(100):
            if 20 <= i < 35:  # 15 measurements from index 20
                value = outlier_value
            else:
                value = random.uniform(sensor.allowed_min, sensor.allowed_max)
            measurements.append(
                MeasurementModel(
                    value=value,
                    unit=MeasurementUnit.CELSIUS,
                    sensor_id=sensor.id,
                    created_at=datetime.now() - timedelta(seconds=30 * i),
                )
            )

        session.add_all(measurements)
        session.flush()


def seed_alarms(session: Session):
    sensor = session.query(SensorModel).first()
    if not sensor:
        _logger.warning("Kein Sensor gefunden, Alarm-Seeding übersprungen.")
        return

    alarm = AlarmModel(
        message="Testalarm: Temperatur out of range",
        severity=AlarmSeverity.HIGH,
        sensor_id=sensor.id,
        created_at=datetime.now(),
    )
    session.add(alarm)
    _logger.info(f"Alarm for sensor {sensor.name} created.")


def seed_users(session: Session):
    keycloak_user_id = UUID(os.environ.get("TEST_USER_KEYCLOAK_ID"))
    email = os.environ.get("TEST_USER_EMAIL")
    name = os.environ.get("TEST_USER_NAME")
    username = os.environ.get("TEST_USER")

    if not keycloak_user_id and not email and not name and not username:
        raise RuntimeError(
            "Seeding dev environment is not configured correctly. Please check environment variables."
        )

    user = (
        session.query(UserModel)
        .filter_by(keycloak_id=str(keycloak_user_id))
        .first()
    )
    if not user:
        user = UserModel(
            keycloak_id=str(keycloak_user_id),
            email=email,
            name=name,
            username=username,
        )
        session.add(user)
        session.flush()

    storage = session.query(StorageModel).first()
    if storage:
        user_storage = UserStorageAccess(
            user_id=user.id,
            storage_id=storage.id,
            role=UserRole.ADMIN,
        )
        session.add(user_storage)
        session.flush()


def seed_dev_data(session: Session):
    """
    Seeds the initial data into the database.
    """
    _logger.info("Seeding random development data...")
    try:
        seed_users(session)
        seed_storages(session)
        seed_sensors(session)
        seed_measurements(session)
        seed_alarms(session)
        seed_users(session)
        session.commit()
        _logger.info("Seeding successful!")
    except Exception as e:
        _logger.error(f"An error occurred during data seeding: {e}")
        session.rollback()
        raise e
