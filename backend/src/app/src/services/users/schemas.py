from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    keycloak_id: str
    username: str
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)