from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.src.app.src.shared.database.enums import MeasurementUnit


class CreateMeasurementRequest(BaseModel):
    value: float
    created_at: datetime
    unit: MeasurementUnit

    model_config = ConfigDict()
