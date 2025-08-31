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

if not all([KEYCLOAK_URL, REALM_NAME, CLIENT_ID]):
    raise RuntimeError(
        "Keycloak is not configured correctly. Please check environment variables."
    )

# URLs for browser flow
AUTHORIZATION_URL = (
    f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/auth"
)
TOKEN_URL = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
# URL for internal service communication
JWKS_URL = f"http://auth.storasense.de:8080/realms/{REALM_NAME}/protocol/openid-connect/certs"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL,
    scopes={"openid": "Standard OpenID Connect scope"},
)


class AuthService:
    def __init__(self):
        # PyJWKClient automatically fetches and caches the JWKS (JSON Web Key Set)
        self.jwks_client = PyJWKClient(JWKS_URL)

    async def validate_token(self, token: str) -> TokenData:
        """
        Validates the JWT token and extracts user information.

        :param token: JWT token from the Authorization header.
        :return: TokenData containing user information.
        """
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated: No token provided.",
            )

        try:
            # Client gets the signing key from token
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)

            # Decrypt payload using the signing key
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                # Checking "Audience": Value of CLIENT_ID must match the "aud" claim in the token.
                audience=CLIENT_ID,
            )

            # Extract information for backend
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
        """
        Dependency to get and validate the current user.

        :param token: JWT token from the Authorization header.
        :return: TokenData containing user information.
        """
        return await self.validate_token(token)


# Global instance of AuthService
auth_service = AuthService()
