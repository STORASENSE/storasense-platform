from fastapi import APIRouter, Request, Depends, HTTPException

from backend.src.app.src.services.auth.service import (
    AuthService,
    inject_auth_service,
)

router = APIRouter(prefix="/auth")


@router.get("/login")
async def login(
    request: Request, auth_service: AuthService = Depends(inject_auth_service)
):
    try:
        return await auth_service.start_login_flow(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Login failed: {e}")


@router.get("/callback", name="auth_callback")
async def auth_callback(
    request: Request, auth_service: AuthService = Depends(inject_auth_service)
):
    try:
        return await auth_service.handle_auth_callback(request)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Authentication failed: {e}"
        )
