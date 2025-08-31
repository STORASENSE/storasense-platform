from typing import Optional
from pydantic import BaseModel


class TokenData(BaseModel):
    id: str  # User ID from Keycloak (subclaim)
    username: str
    email: Optional[str] = None
    name: Optional[str] = None
    client_id: Optional[str] = None
