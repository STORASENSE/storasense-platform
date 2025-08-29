from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AlarmResponse(BaseModel):
    id: UUID
    message: Optional[str] = None
    sensor_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
