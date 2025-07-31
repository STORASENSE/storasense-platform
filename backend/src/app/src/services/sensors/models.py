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


class SensorModel(BaseModel):
    name = None
    __tablename__ = "Sensor"

    type: Mapped[SensorType] = mapped_column(Enum(SensorType))
    storage_id: Mapped[UUID] = mapped_column(ForeignKey("Storage.id"))
    storage: Mapped[StorageModel] = relationship(back_populates="sensors")
    measurements: Mapped[list["MeasurementModel"]] = relationship(
        back_populates="sensor"
    )
