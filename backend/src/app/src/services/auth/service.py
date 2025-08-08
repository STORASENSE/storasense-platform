import os

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, jwk
from jose.exceptions import JWTError

from backend.src.app.src.services.auth.schemas import TokenData

KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL")
REALM_NAME = os.environ.get("KEYCLOAK_REALM")
CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")

if not all([KEYCLOAK_URL, REALM_NAME, CLIENT_ID]):
    raise RuntimeError(
        "Keycloack not properly configured. Please set KEYCLOAK_URL, KEYCLOAK_REALM, and KEYCLOAK_CLIENT_ID environment variables."
    )

# URLS for Keycloak endpoints
AUTHORIZATION_URL = (
    f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/auth"
)
TOKEN_URL = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/certs"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL,
)


class AuthService:
    def __init__(self):
        # Cache for public keys (JWKS) to avoid frequent network calls
        self._jwks_cache = {}

    async def _get_public_key(self, kid: str):
        # gets the public key from the JWKS endpoint to verify JWT signatures
        if not self._jwks_cache:
            async with httpx.AsyncClient() as client:
                response = await client.get(JWKS_URL)
                response.raise_for_status()
                self._jwks_cache = response.json()

        key_data = next(
            (
                key
                for key in self._jwks_cache.get("keys", [])
                if key["kid"] == kid
            ),
            None,
        )
        if not key_data:
            raise HTTPException(
                status_code=401,
                detail="Public Key für die Token-Signatur nicht gefunden.",
            )

        return jwk.construct(key_data)

    async def validate_token(self, token: str) -> TokenData:
        """
        Validates the JWT token and extracts user information.
        Raises HTTPException if the token is invalid or missing required claims.
        """
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Nicht authentifiziert: Kein Token vorhanden.",
            )

        try:
            headers = jwt.get_unverified_headers(token)
            kid = headers.get("kid")
            if not kid:
                raise HTTPException(
                    status_code=401,
                    detail="Token fehlt der 'kid' (Key ID) Header.",
                )

            public_key = await self._get_public_key(kid)

            payload = jwt.decode(
                token,
                public_key.to_pem().decode("utf-8"),
                algorithms=["RS256"],
                audience=CLIENT_ID,
            )

            user_id = payload.get("sub")
            username = payload.get("preferred_username")
            roles = payload.get("realm_access", {}).get("roles", [])

            if not user_id or not username:
                raise HTTPException(
                    status_code=401,
                    detail="Token fehlen wichtige Claims ('sub', 'preferred_username').",
                )

            return TokenData(id=user_id, username=username, roles=roles)

        except JWTError as e:
            raise HTTPException(
                status_code=401, detail=f"Ungültiges Token: {e}"
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme)
    ) -> TokenData:
        """Verifys and returns the current user based on the provided JWT token (auth header)."""
        return await self.validate_token(token)

    def has_role(self, required_role: str):
        async def role_checker(
            token_data: TokenData = Depends(self.get_current_user),
        ):
            if required_role not in token_data.roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Zugriff verweigert: Benötigt Rolle '{required_role}'.",
                )
            return token_data

        return role_checker


# global instance of AuthService for dependency injection
auth_service = AuthService()
