from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.enums import AlarmSeverity

if TYPE_CHECKING:
    from backend.src.app.src.services.sensors.models import (
        SensorModel,
    )


class AlarmModel(BaseModel):
    __tablename__ = "Alarm"

    severity: Mapped[AlarmSeverity] = mapped_column(Enum(AlarmSeverity))
    message: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    sensor_id: Mapped[UUID] = mapped_column(ForeignKey("Sensor.id"))
    sensor: Mapped["SensorModel"] = relationship(back_populates="alarms")
