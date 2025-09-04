import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.users.repository import UserRepository
from backend.src.app.src.services.users.models import UserModel


class TestUserRepository:
    @pytest.fixture
    def mock_session(self):
        mock_session = Mock()
        mock_session.query.return_value = mock_session
        mock_session.scalars.return_value = mock_session
        mock_session.one_or_none.return_value = None
        mock_session.where.return_value = mock_session
        mock_session.filter_by.return_value = mock_session
        mock_session.all.return_value = []
        mock_session.add = Mock()
        return mock_session

    @pytest.fixture
    def user_repository(self, mock_session):
        return UserRepository(mock_session)

    def test_find_by_id_success(self, user_repository, mock_session):
        user_id = uuid4()
        expected_user = Mock()

        mock_session.scalars.return_value.one_or_none.return_value = (
            expected_user
        )

        result = user_repository.find_by_id(user_id)

        assert result == expected_user

    def test_find_by_id_not_found(self, user_repository, mock_session):
        user_id = uuid4()

        mock_session.one_or_none.return_value = None

        result = user_repository.find_by_id(user_id)

        assert result is None

    def test_find_by_keycloak_id_success(self, user_repository, mock_session):
        keycloak_id = "test-keycloak-id"
        expected_user = Mock()

        mock_session.scalars.return_value.one_or_none.return_value = (
            expected_user
        )

        result = user_repository.find_by_keycloak_id(keycloak_id)

        assert result == expected_user

    def test_find_by_keycloak_id_not_found(
        self, user_repository, mock_session
    ):
        keycloak_id = "nonexistent-id"

        mock_session.one_or_none.return_value = None

        result = user_repository.find_by_keycloak_id(keycloak_id)

        assert result is None

    def test_find_by_username_success(self, user_repository, mock_session):
        username = "testuser"
        expected_user = Mock()

        mock_session.one_or_none.return_value = expected_user

        result = user_repository.find_by_username(username)

        assert result == expected_user

    def test_find_by_username_not_found(self, user_repository, mock_session):
        username = "nonexistent"

        mock_session.one_or_none.return_value = None

        result = user_repository.find_by_username(username)

        assert result is None

    def test_find_all_by_storage_id(self, user_repository, mock_session):
        storage_id = uuid4()
        expected_users = [Mock(), Mock()]

        mock_session.join.return_value = mock_session
        mock_session.filter_by.return_value = mock_session
        mock_session.all.return_value = expected_users

        result = user_repository.find_all_by_storage_id(storage_id)

        assert result == expected_users

    def test_create_user(self, user_repository, mock_session):
        user_data = {
            "keycloak_id": "test-id",
            "username": "testuser",
            "email": "test@example.com",
            "name": "Test User",
        }

        result = user_repository.create_user(user_data)

        assert isinstance(result, UserModel)
        mock_session.add.assert_called_once_with(result)
