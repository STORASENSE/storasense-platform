from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.enums import MeasurementUnit

if TYPE_CHECKING:
    from backend.src.app.src.services.sensors.models import SensorModel


class MeasurementModel(BaseModel):
    __tablename__ = "Measurements"
    __timescaledb_hypertable__ = {"time_column_name": "timestamp"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    timestamp: Mapped[datetime] = mapped_column(
        primary_key=True
    )  # Composite PK
    value: Mapped[float] = mapped_column()
    unit: Mapped[MeasurementUnit] = mapped_column(Enum(MeasurementUnit))
    sensor_id: Mapped[UUID] = mapped_column(
        ForeignKey("Sensor.id", ondelete="CASCADE")
    )  # cascade: delete measurements when sensor is deleted
    sensor: Mapped["SensorModel"] = relationship(back_populates="measurements")
