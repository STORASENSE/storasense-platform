# Pydantic-based models
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StorageResponse(BaseModel):
    id: UUID
    name: Optional[str]

    model_config = ConfigDict()


class CreateStorageRequest(BaseModel):
    name: str
