from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    keycloak_id: str
    username: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    description: Optional[str] = None
    roles: List[str]

    model_config = ConfigDict(from_attributes=True)
