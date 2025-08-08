from typing import List
from pydantic import BaseModel


class TokenData(BaseModel):
    id: str  # User ID from Keycloak (sub claim)
    username: str
    roles: List[str]
