from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.src.app.src.shared.database.enums import AlarmSeverity


class AlarmResponse(BaseModel):
    """Response schema for alarm data."""

    id: UUID
    severity: AlarmSeverity
    message: Optional[str] = None
    sensor_id: UUID
    measurement_id: UUID
    measurement_created_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict()
