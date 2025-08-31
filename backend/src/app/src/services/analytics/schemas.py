from typing import Literal
from pydantic import BaseModel

# Allowed windows for analytics queries
Window = Literal["7d", "30d", "365d"]


class DoorOpenItem(BaseModel):
    day: str
    sensor_id: str
    open_seconds: int


class SummaryItem(BaseModel):
    type: str
    sensor_id: str
    avg_value: float
    min_value: float
    max_value: float
