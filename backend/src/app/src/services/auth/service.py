import os
from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

from backend.src.app.src.services.users.service import (
    UserService,
    inject_user_service,
)


class AuthService:
    def __init__(self, user_service: UserService):
        self._user_service = user_service
        self.oauth = OAuth()

        self.oauth.register(
            name="tinyauth",
            client_id=os.environ.get("OIDC_CLIENT_ID"),
            client_secret=os.environ.get("OIDC_CLIENT_SECRET"),
            authorize_url=os.environ.get("OIDC_AUTHORIZE_URL"),
            access_token_url=os.environ.get("OIDC_TOKEN_URL"),
            userinfo_endpoint=os.environ.get("OIDC_USERINFO_URL"),
            client_kwargs={"scope": "openid email profile"},
        )

    async def start_login_flow(self, request: Request) -> RedirectResponse:
        redirect_uri = request.url_for("auth_callback")

        return await self.oauth.tinyauth.authorize_redirect(
            request, redirect_uri
        )

    async def handle_auth_callback(self, request: Request) -> RedirectResponse:
        token = await self.oauth.tinyauth.authorize_access_token(request)

        user_info = token.get("userinfo")
        if not user_info and "id_token" in token:
            user_info = await self.oauth.tinyauth.parse_id_token(
                request, token
            )

        if user_info:
            local_user = self._user_service.get_or_create_user_from_oidc(
                user_info
            )

            request.session["user_id"] = str(local_user.id)
            request.session["email"] = local_user.email

        return RedirectResponse(url="http://app.storasense.de/docs")


def inject_auth_service(
    user_service: UserService = Depends(inject_user_service),
) -> AuthService:
    return AuthService(user_service=user_service)
