from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Enum, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.enums import AlarmSeverity

if TYPE_CHECKING:
    from backend.src.app.src.services.measurements.models import (
        MeasurementModel,
    )


class AlarmModel(BaseModel):
    __tablename__ = "Alarm"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    severity: Mapped[AlarmSeverity] = mapped_column(Enum(AlarmSeverity))
    message: Mapped[Optional[str]] = mapped_column()
    measurement_id: Mapped[UUID] = mapped_column()
    measurement_created_at: Mapped[datetime] = mapped_column()

    __table_args__ = (
        ForeignKeyConstraint(
            ["measurement_id", "measurement_created_at"],
            ["Measurements.id", "Measurements.created_at"],
        ),
    )

    measurement: Mapped["MeasurementModel"] = relationship(
        back_populates="alarm"
    )
