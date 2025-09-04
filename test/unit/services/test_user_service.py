import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.users.service import (
    UserService,
    is_technical_user,
)
from backend.src.app.src.services.users.schemas import UserByStorageIdResponse
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
)
from backend.src.app.src.services.users.errors import UserDoesNotExistError
from backend.src.app.src.shared.database.enums import UserRole


class TestUserService:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def mock_user_repository(self):
        return Mock()

    @pytest.fixture
    def mock_storage_repository(self):
        return Mock()

    @pytest.fixture
    def mock_user_storage_access_repository(self):
        return Mock()

    @pytest.fixture
    def user_service(
        self,
        mock_session,
        mock_user_repository,
        mock_storage_repository,
        mock_user_storage_access_repository,
    ):
        return UserService(
            mock_session,
            mock_user_repository,
            mock_storage_repository,
            mock_user_storage_access_repository,
        )

    @pytest.fixture
    def token_data(self):
        return TokenData(
            id="test-keycloak-id",
            username="testuser",
            email="test@example.com",
            name="Test User",
            client_id="test-client",
        )

    @pytest.fixture
    def technical_token_data(self):
        return TokenData(
            id="technical-user-id",
            username="technical-user",
            email=None,
            name=None,
            client_id="technical-client",
        )

    def test_is_technical_user_true(self, technical_token_data):
        assert is_technical_user(technical_token_data) is True

    def test_is_technical_user_false(self, token_data):
        assert is_technical_user(token_data) is False

    def test_get_or_create_user_by_keycloak_id_existing_user(
        self, user_service, mock_user_repository, token_data
    ):
        existing_user = Mock()
        mock_user_repository.find_by_keycloak_id.return_value = existing_user

        result = user_service.get_or_create_user_by_keycloak_id(token_data)

        assert result == existing_user
        mock_user_repository.find_by_keycloak_id.assert_called_once_with(
            token_data.id
        )

    def test_get_or_create_user_by_keycloak_id_new_regular_user(
        self, user_service, mock_session, mock_user_repository, token_data
    ):
        mock_user_repository.find_by_keycloak_id.return_value = None
        new_user = Mock()
        mock_user_repository.create_user.return_value = new_user

        result = user_service.get_or_create_user_by_keycloak_id(token_data)

        assert result == new_user
        expected_user_data = {
            "keycloak_id": token_data.id,
            "username": token_data.username,
            "email": token_data.email,
            "name": token_data.name,
        }
        mock_user_repository.create_user.assert_called_once_with(
            expected_user_data
        )
        mock_session.commit.assert_called_once()

    def test_get_or_create_user_by_keycloak_id_new_technical_user(
        self,
        user_service,
        mock_session,
        mock_user_repository,
        technical_token_data,
    ):
        mock_user_repository.find_by_keycloak_id.return_value = None
        new_user = Mock()
        mock_user_repository.create_user.return_value = new_user

        result = user_service.get_or_create_user_by_keycloak_id(
            technical_token_data
        )

        assert result == new_user
        expected_user_data = {
            "keycloak_id": technical_token_data.id,
            "username": technical_token_data.username,
        }
        mock_user_repository.create_user.assert_called_once_with(
            expected_user_data
        )
        mock_session.commit.assert_called_once()

    def test_find_all_by_storage_id_success(
        self,
        user_service,
        mock_user_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        storage_id = uuid4()
        user_id = uuid4()

        principal = Mock()
        principal.id = user_id
        principal.username = "testuser"
        users = [principal]

        mock_user_repository.find_by_keycloak_id.return_value = principal
        mock_user_repository.find_all_by_storage_id.return_value = users
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )

        result = user_service.find_all_by_storage_id(storage_id, token_data)

        assert len(result) == 1
        assert isinstance(result[0], UserByStorageIdResponse)
        assert result[0].id == user_id
        assert result[0].role == UserRole.ADMIN

    def test_find_all_by_storage_id_unauthorized(
        self, user_service, mock_user_repository, token_data
    ):
        storage_id = uuid4()

        principal = Mock()
        other_user = Mock()
        users = [other_user]

        mock_user_repository.find_by_keycloak_id.return_value = principal
        mock_user_repository.find_all_by_storage_id.return_value = users

        with pytest.raises(AuthorizationError):
            user_service.find_all_by_storage_id(storage_id, token_data)

    def test_add_user_to_storage_success(
        self,
        user_service,
        mock_session,
        mock_user_repository,
        mock_storage_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        username = "newuser"
        storage_id = uuid4()
        user_id = uuid4()
        principal_id = uuid4()

        principal = Mock()
        principal.id = principal_id
        user_to_add = Mock()
        user_to_add.id = user_id

        mock_user_repository.find_by_keycloak_id.return_value = principal
        mock_user_repository.find_by_username.return_value = user_to_add
        mock_storage_repository.exists.return_value = True
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )

        user_service.add_user_to_storage(username, storage_id, token_data)

        mock_user_storage_access_repository.add_user_to_storage.assert_called_once_with(
            user_id, storage_id, UserRole.CONTRIBUTOR
        )
        mock_session.commit.assert_called_once()

    def test_add_user_to_storage_user_not_found(
        self,
        user_service,
        mock_user_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        username = "nonexistent"
        storage_id = uuid4()
        principal_id = uuid4()

        principal = Mock()
        principal.id = principal_id

        mock_user_repository.find_by_keycloak_id.return_value = principal
        mock_user_repository.find_by_username.return_value = None
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )

        with pytest.raises(UserDoesNotExistError):
            user_service.add_user_to_storage(username, storage_id, token_data)

    def test_remove_user_from_storage_success(
        self,
        user_service,
        mock_session,
        mock_user_repository,
        mock_storage_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        username = "usertoremove"
        storage_id = uuid4()
        user_id = uuid4()
        principal_id = uuid4()

        principal = Mock()
        principal.id = principal_id
        user_to_remove = Mock()
        user_to_remove.id = user_id

        mock_user_repository.find_by_keycloak_id.return_value = principal
        mock_user_repository.find_by_username.return_value = user_to_remove
        mock_storage_repository.exists.return_value = True
        mock_user_storage_access_repository.find_user_role.side_effect = [
            UserRole.ADMIN,  # principal role
            UserRole.CONTRIBUTOR,  # user to remove role
        ]

        user_service.remove_user_from_storage(username, storage_id, token_data)

        mock_user_storage_access_repository.remove_user_from_storage.assert_called_once_with(
            user_id, storage_id
        )
        mock_session.commit.assert_called_once()

    def test_remove_user_from_storage_cannot_remove_admin(
        self,
        user_service,
        mock_user_repository,
        mock_storage_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        username = "adminuser"
        storage_id = uuid4()
        user_id = uuid4()
        principal_id = uuid4()

        principal = Mock()
        principal.id = principal_id
        admin_user = Mock()
        admin_user.id = user_id

        mock_user_repository.find_by_keycloak_id.return_value = principal
        mock_user_repository.find_by_username.return_value = admin_user
        mock_user_storage_access_repository.find_user_role.side_effect = [
            UserRole.ADMIN,  # principal role
            UserRole.ADMIN,  # user to remove role
        ]

        with pytest.raises(AuthorizationError):
            user_service.remove_user_from_storage(
                username, storage_id, token_data
            )
