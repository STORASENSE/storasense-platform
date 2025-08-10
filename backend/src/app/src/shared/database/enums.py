from enum import Enum


class UserRole(Enum):
    ADMIN = "ADMIN"
    CONTRIBUTOR = "CONTRIBUTOR"


class SensorType(Enum):
    TEMPERATURE_INSIDE = "TEMPERATURE_INSIDE"
    TEMPERATURE_OUTSIDE = "TEMPERATURE_OUTSIDE"
    HUMIDITY = "HUMIDITY"
    GAS = "GAS"
    ULTRASONIC = "ULTRASONIC"


class MeasurementUnit(Enum):
    CELSIUS = "CELSIUS"
    FAHRENHEIT = "FAHRENHEIT"
    PERCENT = "PERCENT"


class AlarmSeverity(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
