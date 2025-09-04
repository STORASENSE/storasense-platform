import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.user_storage_access.repository import (
    UserStorageAccessRepository,
)
from backend.src.app.src.shared.database.enums import UserRole


class TestUserStorageAccessRepository:
    @pytest.fixture
    def mock_session(self):
        mock_session = Mock()
        mock_session.query.return_value = mock_session
        mock_session.where.return_value = mock_session
        mock_session.one_or_none.return_value = None
        mock_session.filter.return_value = mock_session
        mock_session.first.return_value = None
        mock_session.delete = Mock()
        mock_session.add = Mock()
        return mock_session

    @pytest.fixture
    def user_storage_access_repository(self, mock_session):
        repo = UserStorageAccessRepository(mock_session)
        repo.exists = Mock(return_value=False)
        repo.create = Mock()
        repo.delete_by_id = Mock()
        return repo

    def test_find_user_role_admin(
        self, user_storage_access_repository, mock_session
    ):
        user_id = uuid4()
        storage_id = uuid4()

        mock_access = Mock()
        mock_access.role = UserRole.ADMIN
        mock_session.one_or_none.return_value = mock_access

        result = user_storage_access_repository.find_user_role(
            user_id, storage_id
        )

        assert result == UserRole.ADMIN

    def test_find_user_role_contributor(
        self, user_storage_access_repository, mock_session
    ):
        user_id = uuid4()
        storage_id = uuid4()

        mock_access = Mock()
        mock_access.role = UserRole.CONTRIBUTOR
        mock_session.one_or_none.return_value = mock_access

        result = user_storage_access_repository.find_user_role(
            user_id, storage_id
        )

        assert result == UserRole.CONTRIBUTOR

    def test_find_user_role_not_found(
        self, user_storage_access_repository, mock_session
    ):
        user_id = uuid4()
        storage_id = uuid4()

        mock_session.one_or_none.return_value = None

        result = user_storage_access_repository.find_user_role(
            user_id, storage_id
        )

        assert result is None

    def test_add_user_to_storage(
        self, user_storage_access_repository, mock_session
    ):
        user_id = uuid4()
        storage_id = uuid4()
        role = UserRole.CONTRIBUTOR

        user_storage_access_repository.add_user_to_storage(
            user_id, storage_id, role
        )

        user_storage_access_repository.create.assert_called_once()

    def test_remove_user_from_storage(
        self, user_storage_access_repository, mock_session
    ):
        user_id = uuid4()
        storage_id = uuid4()

        user_storage_access_repository.exists.return_value = True

        user_storage_access_repository.remove_user_from_storage(
            user_id, storage_id
        )

        user_storage_access_repository.delete_by_id.assert_called_once_with(
            (user_id, storage_id)
        )
