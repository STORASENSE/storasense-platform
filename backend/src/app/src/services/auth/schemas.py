from typing import List, Optional
from pydantic import BaseModel


class TokenData(BaseModel):
    id: str  # User ID from Keycloak (subclaim)
    username: str
    roles: List[str]
    email: Optional[str] = None
    name: Optional[str] = None
