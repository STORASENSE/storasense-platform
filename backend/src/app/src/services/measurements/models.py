from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.enums import MeasurementUnit

if TYPE_CHECKING:
    from backend.src.app.src.services.alarms.models import AlarmModel
    from backend.src.app.src.services.sensors.models import SensorModel


class MeasurementModel(BaseModel):
    __tablename__ = "Measurement"

    value: Mapped[float] = mapped_column()
    unit: Mapped[MeasurementUnit] = mapped_column(Enum(MeasurementUnit))
    created_at: Mapped[datetime] = mapped_column()
    sensor_id: Mapped[UUID] = mapped_column(ForeignKey("Sensor.id"))
    sensor: Mapped["SensorModel"] = relationship(back_populates="measurements")
    alarm: Mapped[Optional["AlarmModel"]] = relationship(
        back_populates="measurement"
    )
