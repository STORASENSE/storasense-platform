from enum import Enum


class UserRole(Enum):
    ADMIN = "ADMIN"
    CONTRIBUTOR = "CONTRIBUTOR"


class SensorType(Enum):
    TEMPERATURE_INSIDE = "TEMPERATURE_INSIDE"
    TEMPERATURE_OUTSIDE = "TEMPERATURE_OUTSIDE"
    HUMIDITY = "HUMIDITY"
    GAS = "CO2"
    ULTRASONIC = "ULTRASONIC"


class MeasurementUnit(Enum):
    CELSIUS = "CELSIUS"
    FAHRENHEIT = "FAHRENHEIT"
    PERCENT = "PERCENT"
    CENTIMETER = "CENTIMETER"
    PPM = "PPM"


class AlarmSeverity(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
