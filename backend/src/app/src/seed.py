from sqlalchemy.orm import Session
from uuid import UUID

from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.shared.database.enums import SensorType


def seed_initial_data(session: Session):
    """
    Seeds the initial data into the database.
    """
    try:
        print("Seeding initial data...")

        initial_storage = StorageModel(
            id=UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"), name="Hauptlager"
        )
        print(f"Preparing to seed storage: '{initial_storage.name}'")

        # Define 5 sensors with predefined values
        sensors_to_create = [
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "Temperature-Inside",
                "type": SensorType.TEMPERATURE,
                "allowed_min": 0.0,
                "allowed_max": 40.0,
            },
            {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Humidity",
                "type": SensorType.HUMIDITY,
                "allowed_min": 20.0,
                "allowed_max": 80.0,
            },
            {
                "id": "00000000-0000-0000-0000-000000000003",
                "name": "Ultrasonic",
                "type": SensorType.ULTRASONIC,
                "allowed_min": 100.0,
                "allowed_max": 100.0,
            },
            {
                "id": "00000000-0000-0000-0000-000000000004",
                "name": "Temperature-Outside",
                "type": SensorType.TEMPERATURE,
                "allowed_min": -10.0,
                "allowed_max": 50.0,
            },
            {
                "id": "00000000-0000-0000-0000-000000000005",
                "name": "Air",
                "type": SensorType.AIR,
                "allowed_min": 10.0,
                "allowed_max": 20.0,
            },
        ]

        created_sensors = []
        for sensor_data in sensors_to_create:
            new_sensor = SensorModel(
                id=UUID(sensor_data["id"]),
                name=sensor_data["name"],
                type=sensor_data["type"],
                storage_id=initial_storage.id,
                allowed_min=sensor_data["allowed_min"],
                allowed_max=sensor_data["allowed_max"],
            )
            created_sensors.append(new_sensor)
            print(
                f"  - Preparing sensor: '{new_sensor.name}' with Min/Max: {new_sensor.allowed_min}/{new_sensor.allowed_max}"
            )

        session.add(initial_storage)
        session.add_all(created_sensors)

        session.commit()
        print(
            f"Successfully seeded 1 storage and {len(created_sensors)} sensors with predefined IDs and limits."
        )

    except Exception as e:
        print(f"An error occurred during data seeding: {e}")
        session.rollback()
