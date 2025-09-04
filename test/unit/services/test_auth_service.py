import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
import jwt

from backend.src.app.src.services.auth.service import AuthService
from backend.src.app.src.services.auth.schemas import TokenData


class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        with patch(
            "backend.src.app.src.services.auth.service.PyJWKClient"
        ) as mock_jwks_client:
            service = AuthService()
            service.jwks_client = mock_jwks_client.return_value
            return service

    @pytest.fixture
    def valid_token_payload(self):
        return {
            "sub": "test-user-id",
            "preferred_username": "testuser",
            "email": "test@example.com",
            "name": "Test User",
            "clientId": "test-client",
        }

    @pytest.mark.asyncio
    async def test_validate_token_success(
        self, auth_service, valid_token_payload
    ):
        token = "valid.jwt.token"
        mock_signing_key = Mock()
        mock_signing_key.key = "test-key"

        auth_service.jwks_client.get_signing_key_from_jwt.return_value = (
            mock_signing_key
        )

        with patch("jwt.decode", return_value=valid_token_payload):
            result = await auth_service.validate_token(token)

            assert isinstance(result, TokenData)
            assert result.id == "test-user-id"
            assert result.username == "testuser"
            assert result.email == "test@example.com"
            assert result.name == "Test User"
            assert result.client_id == "test-client"

    @pytest.mark.asyncio
    async def test_validate_token_no_token(self, auth_service):
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.validate_token("")

        assert exc_info.value.status_code == 401
        assert "Not authenticated: No token provided" in str(
            exc_info.value.detail
        )

    @pytest.mark.asyncio
    async def test_validate_token_missing_required_claims(self, auth_service):
        token = "invalid.jwt.token"
        mock_signing_key = Mock()
        mock_signing_key.key = "test-key"

        auth_service.jwks_client.get_signing_key_from_jwt.return_value = (
            mock_signing_key
        )

        payload_missing_sub = {
            "preferred_username": "testuser",
            "email": "test@example.com",
        }

        with patch("jwt.decode", return_value=payload_missing_sub):
            with pytest.raises(HTTPException) as exc_info:
                await auth_service.validate_token(token)

            assert exc_info.value.status_code == 401
            assert "missing required claims" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_validate_token_jwt_decode_error(self, auth_service):
        token = "invalid.jwt.token"
        mock_signing_key = Mock()
        mock_signing_key.key = "test-key"

        auth_service.jwks_client.get_signing_key_from_jwt.return_value = (
            mock_signing_key
        )

        with patch("jwt.decode", side_effect=jwt.PyJWTError("Invalid token")):
            with pytest.raises(HTTPException) as exc_info:
                await auth_service.validate_token(token)

            assert exc_info.value.status_code == 401
            assert "Invalid token" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_current_user(self, auth_service, valid_token_payload):
        token = "valid.jwt.token"
        mock_signing_key = Mock()
        mock_signing_key.key = "test-key"

        auth_service.jwks_client.get_signing_key_from_jwt.return_value = (
            mock_signing_key
        )

        with patch("jwt.decode", return_value=valid_token_payload):
            result = await auth_service.get_current_user(token)

            assert isinstance(result, TokenData)
            assert result.id == "test-user-id"
            assert result.username == "testuser"
