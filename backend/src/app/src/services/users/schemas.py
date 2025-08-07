from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: Optional[str] = None
    role: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
