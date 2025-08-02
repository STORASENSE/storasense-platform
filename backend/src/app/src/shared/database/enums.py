from enum import Enum


class UserRole(Enum):
    ADMIN = "ADMIN"
    CONTRIBUTOR = "CONTRIBUTOR"


class SensorType(Enum):
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"


class MeasurementUnit(Enum):
    CELSIUS = "CELSIUS"
    FAHRENHEIT = "FAHRENHEIT"
    PERCENT = "PERCENT"


class AlarmSeverity(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
