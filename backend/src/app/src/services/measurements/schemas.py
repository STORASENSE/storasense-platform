from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.src.app.src.shared.database.enums import MeasurementUnit


class CreateMeasurementRequest(BaseModel):
    value: float
    created_at: datetime
    unit: MeasurementUnit

    model_config = ConfigDict()


class MeasurementResponse(BaseModel):
    id: UUID
    value: float
    unit: MeasurementUnit
    created_at: datetime

    class Config:
        from_attributes = True


class GetMeasurementsResponse(BaseModel):
    measurements: list[MeasurementResponse]

    model_config = ConfigDict()
