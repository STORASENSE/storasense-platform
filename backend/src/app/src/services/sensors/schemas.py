from uuid import UUID
from pydantic import BaseModel, ConfigDict

from backend.src.app.src.shared.database.enums import SensorType


class CreateSensorRequest(BaseModel):
    storage_id: UUID
    type: SensorType
    name: str | None = None
    allowed_min: float | None = None
    allowed_max: float | None = None


class SensorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str | None
    type: SensorType
    storage_id: UUID
