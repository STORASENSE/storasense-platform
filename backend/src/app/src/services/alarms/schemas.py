from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.src.app.src.shared.database.enums import AlarmSeverity


class AlarmResponse(BaseModel):
    id: UUID
    severity: AlarmSeverity
    message: Optional[str] = None
    sensor_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
