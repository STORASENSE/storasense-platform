import os
import jwt
from jwt import PyJWKClient

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer

from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.shared.logger import get_logger

_logger = get_logger(__name__)

KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL")
REALM_NAME = os.environ.get("KEYCLOAK_REALM")
CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")
MQTT_CLIENT_ID = os.environ.get("MQTT_CLIENT_ID")
ALLOWED_AUDIENCES = set(
    filter(
        None,
        [
            CLIENT_ID,
            MQTT_CLIENT_ID,
        ],
    )
)
if not all([KEYCLOAK_URL, REALM_NAME, CLIENT_ID]):
    raise RuntimeError(
        "Keycloak is not configured correctly. Please check environment variables."
    )

AUTHORIZATION_URL = (
    f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/auth"
)
TOKEN_URL = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
JWKS_URL = f"http://auth.storasense.de:8080/realms/{REALM_NAME}/protocol/openid-connect/certs"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL,
    scopes={"openid": "Standard OpenID Connect scope"},
)


class AuthService:
    def __init__(self):
        self.jwks_client = PyJWKClient(JWKS_URL)

    async def validate_token(self, token: str) -> TokenData:
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated: No token provided.",
            )

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=None,
            )

            aud = payload.get("aud")
            if isinstance(aud, list):
                if not any(a in ALLOWED_AUDIENCES for a in aud):
                    raise HTTPException(
                        status_code=401, detail="Invalid audience"
                    )
            elif aud not in ALLOWED_AUDIENCES:
                raise HTTPException(status_code=401, detail="Invalid audience")

            user_id = payload.get("sub")
            username = payload.get("preferred_username")
            roles = payload.get("realm_access", {}).get("roles", [])
            email = payload.get("email")
            name = payload.get("name")

            if not user_id or not username:
                raise HTTPException(
                    status_code=401,
                    detail="Token is missing required claims ('sub', 'preferred_username').",
                )

            return TokenData(
                id=user_id,
                username=username,
                roles=roles,
                email=email,
                name=name,
            )

        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme)
    ) -> TokenData:
        return await self.validate_token(token)

    def has_role(self, required_role: str):
        async def role_checker(
            token_data: TokenData = Depends(self.get_current_user),
        ):
            if required_role not in token_data.roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Access denied: Requires role '{required_role}'.",
                )
            return token_data

        return role_checker


auth_service = AuthService()
