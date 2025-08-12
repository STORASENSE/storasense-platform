import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from uuid import UUID

from backend.src.app.src.shared.logging import logging
from backend.src.app.src.services.measurements.models import MeasurementModel
from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.shared.database.enums import (
    SensorType,
    MeasurementUnit,
)


_logger = logging.getLogger(__name__)


def seed_users(session: Session):
    pass


def seed_storages(session: Session):
    storages: list[StorageModel] = [
        StorageModel(
            id=UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"),
            name="MyStorage",
            password_hash="1234",
            password_salt="1234",
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
    pass


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
        session.commit()
        _logger.info("Seeding successful!")
    except Exception as e:
        _logger.error(f"An error occurred during data seeding: {e}")
        session.rollback()
        raise e
