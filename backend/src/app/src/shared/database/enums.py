from enum import Enum


class UserRole(Enum):
    ADMIN = "ADMIN"
    CONTRIBUTOR = "CONTRIBUTOR"


class SensorType(Enum):
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    ULTRASONIC = "ULTRASONIC"
    AIR = "AIR"


class MeasurementUnit(Enum):
    CELSIUS = "CELSIUS"
    FAHRENHEIT = "FAHRENHEIT"
    PERCENT = "PERCENT"


class AlarmSeverity(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
