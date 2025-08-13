from sqlalchemy.orm import Session
from uuid import UUID

from backend.src.app.src.shared.logger import get_logger
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.shared.database.enums import SensorType


_logger = get_logger(__name__)

_known_storage_id = UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")


def seed_storage(session: Session):
    _logger.info("Seeding storage...")
    initial_storage = StorageModel(
        id=_known_storage_id,
        name="Main Storage",
        password_hash="1234",
        password_salt="1234",
    )
    session.add(initial_storage)
    session.flush()
    _logger.info("Storage seeded successfully!")


def seed_sensors(session: Session):
    _logger.info("Seeding sensors for created storage...")
    temp_inside = SensorModel(
        id=UUID("3f8f788a-a6d0-34ee-9cc0-2a762338cfda"),
        name="Temperature (Inside)",
        type=SensorType.TEMPERATURE_INSIDE,
        storage_id=_known_storage_id,
        allowed_min=1.0,
        allowed_max=5.0,
    )
    temp_outside = SensorModel(
        id=UUID("e2cab404-1e6b-31f1-8f90-840273670527"),
        name="Temperature (Outside)",
        type=SensorType.TEMPERATURE_OUTSIDE,
        storage_id=_known_storage_id,
        allowed_min=-10.0,
        allowed_max=40.0,
    )
    humidity = SensorModel(
        id=UUID("9f34ef74-445a-3aef-8ecd-2b9803062cbf"),
        name="Humidity",
        type=SensorType.HUMIDITY,
        storage_id=_known_storage_id,
        allowed_min=20.0,
        allowed_max=80.0,
    )
    ultrasonic = SensorModel(
        id=UUID("ad5b8443-aef7-39a8-a530-75282ecb075f"),
        name="Ultrasonic",
        type=SensorType.ULTRASONIC,
        storage_id=_known_storage_id,
        allowed_min=100.0,
        allowed_max=100.0,
    )
    air = SensorModel(
        id=UUID("86c9381d-7265-3f3b-bef2-68b9742d30b9"),
        name="Air Quality",
        type=SensorType.GAS,
        storage_id=_known_storage_id,
        allowed_min=10.0,
        allowed_max=20.0,
    )
    session.add_all([temp_inside, temp_outside, humidity, ultrasonic, air])
    session.flush()
    _logger.info("Sensors seeded successfully!")


def seed_prod_data(session: Session):
    """
    Seeds the initial data into the database.
    """
    _logger.info("Seeding production data...")
    try:
        seed_storage(session)
        seed_sensors(session)
        session.commit()
        _logger.info("Production seeding successful!")
    except Exception as e:
        _logger.error(f"An error occurred during data seeding: {e}")
        session.rollback()
        raise e
