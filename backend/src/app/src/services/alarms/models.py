from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel

if TYPE_CHECKING:
    from backend.src.app.src.services.sensors.models import (
        SensorModel,
    )


class AlarmModel(BaseModel):
    __tablename__ = "Alarm"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    message: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    sensor_id: Mapped[UUID] = mapped_column(ForeignKey("Sensor.id"))
    sensor: Mapped["SensorModel"] = relationship(back_populates="alarms")
