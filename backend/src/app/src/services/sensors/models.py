from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.enums import SensorType

if TYPE_CHECKING:
    from backend.src.app.src.services.measurements.models import (
        MeasurementModel,
    )
    from backend.src.app.src.services.alarms.models import (
        AlarmModel,
    )


class SensorModel(BaseModel):
    __tablename__ = "Sensor"

    type: Mapped[SensorType] = mapped_column(Enum(SensorType))
    name: Mapped[str] = mapped_column(nullable=True)
    storage_id: Mapped[UUID] = mapped_column(ForeignKey("Storage.id"))
    storage: Mapped[StorageModel] = relationship(back_populates="sensors")
    allowed_min: Mapped[float] = mapped_column(nullable=True)
    allowed_max: Mapped[float] = mapped_column(nullable=True)
    measurements: Mapped[list["MeasurementModel"]] = relationship(
        back_populates="sensor",
        cascade="all",  # Cascade: delete measurements when sensor is deleted
    )
    alarms: Mapped[list["AlarmModel"]] = relationship(back_populates="sensor")
