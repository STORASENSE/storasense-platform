from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    keycloak_id: str
    username: str
    email: Optional[str] = (
        None  # Allow null for email to support technical users
    )
    name: Optional[str] = (
        None  # Allow null for name to support technical users
    )

    model_config = ConfigDict(from_attributes=True)


class UserPublicResponse(BaseModel):
    """Public User Response Schema"""

    username: str
    email: Optional[str] = None
    name: Optional[str] = None
