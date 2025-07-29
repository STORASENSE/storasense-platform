from backend.src.app.src.services.users.models import UserModel
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.services.sensors.models import SensorModel
from backend.src.app.src.services.measurements.models import MeasurementModel
from backend.src.app.src.services.alarms.models import AlarmModel


def discover_models():
    """
    This method does absolutely nothing, but importing this module is needed for discovering all
    database models. This function should be called once at the start of the application.
    """
    pass


__all__ = [
    "discover_models",
    "UserModel",
    "StorageModel",
    "SensorModel",
    "MeasurementModel",
    "AlarmModel",
]
