from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.enums import AlarmSeverity

if TYPE_CHECKING:
    from backend.src.app.src.services.measurements.models import (
        MeasurementModel,
    )


class AlarmModel(BaseModel):
    __tablename__ = "Alarm"

    severity: Mapped[AlarmSeverity] = mapped_column(Enum(AlarmSeverity))
    message: Mapped[Optional[str]] = mapped_column()
    measurement_id: Mapped[UUID] = mapped_column(ForeignKey("Measurement.id"))
    measurement: Mapped["MeasurementModel"] = relationship(
        back_populates="alarm"
    )
