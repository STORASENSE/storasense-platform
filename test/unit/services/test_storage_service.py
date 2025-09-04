import pytest
from unittest.mock import Mock
from uuid import uuid4

from backend.src.app.src.services.storages.service import StorageService
from backend.src.app.src.services.auth.schemas import TokenData
from backend.src.app.src.services.auth.errors import (
    AuthorizationError,
    UnknownAuthPrincipalError,
)
from backend.src.app.src.services.storages.errors import (
    StorageAlreadyExistsError,
    StorageNotFoundError,
)
from backend.src.app.src.shared.database.enums import UserRole


class TestStorageService:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def mock_storage_repository(self):
        return Mock()

    @pytest.fixture
    def mock_user_repository(self):
        return Mock()

    @pytest.fixture
    def mock_user_storage_access_repository(self):
        return Mock()

    @pytest.fixture
    def storage_service(
        self,
        mock_session,
        mock_storage_repository,
        mock_user_repository,
        mock_user_storage_access_repository,
    ):
        return StorageService(
            mock_session,
            mock_storage_repository,
            mock_user_repository,
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

    def test_find_storages_by_user_id(
        self, storage_service, mock_storage_repository
    ):
        user_id = uuid4()
        expected_storages = [Mock(), Mock()]

        mock_storage_repository.find_all_by_user_id.return_value = (
            expected_storages
        )

        result = storage_service.find_storages_by_user_id(user_id)

        assert result == expected_storages
        mock_storage_repository.find_all_by_user_id.assert_called_once_with(
            user_id
        )

    def test_find_my_storages_success(
        self,
        storage_service,
        mock_user_repository,
        mock_storage_repository,
        token_data,
    ):
        user_id = uuid4()
        user = Mock()
        user.id = user_id
        expected_storages = [Mock(), Mock()]

        mock_user_repository.find_by_keycloak_id.return_value = user
        mock_storage_repository.find_all_by_user_id.return_value = (
            expected_storages
        )

        result = storage_service.find_my_storages(token_data)

        assert result == expected_storages
        mock_user_repository.find_by_keycloak_id.assert_called_once_with(
            token_data.id
        )
        mock_storage_repository.find_all_by_user_id.assert_called_once_with(
            user_id
        )

    def test_find_my_storages_user_not_found(
        self, storage_service, mock_user_repository, token_data
    ):
        mock_user_repository.find_by_keycloak_id.return_value = None

        with pytest.raises(UnknownAuthPrincipalError):
            storage_service.find_my_storages(token_data)

    def test_create_storage_success(
        self,
        storage_service,
        mock_user_repository,
        mock_storage_repository,
        token_data,
    ):
        from uuid import uuid4
        from unittest.mock import Mock, patch

        user_id = uuid4()
        user = Mock()
        user.id = user_id
        storage = Mock()
        storage.id = None
        storage.user_associations = []

        mock_user_repository.find_by_keycloak_id.return_value = user

        # Mock the UserStorageAccessModel creation to avoid SQLAlchemy issues
        with patch(
            "backend.src.app.src.services.storages.service.UserStorageAccessModel"
        ) as mock_model:
            mock_association = Mock()
            mock_model.return_value = mock_association

            storage_service.create_storage(storage, token_data)

            assert len(storage.user_associations) == 1
            mock_storage_repository.create.assert_called_once_with(storage)
            storage_service.session.commit.assert_called_once()

    def test_create_storage_user_not_found(
        self, storage_service, mock_user_repository, token_data
    ):
        storage = Mock()
        mock_user_repository.find_by_keycloak_id.return_value = None

        with pytest.raises(UnknownAuthPrincipalError):
            storage_service.create_storage(storage, token_data)

    def test_create_storage_already_exists(
        self,
        storage_service,
        mock_user_repository,
        mock_storage_repository,
        token_data,
    ):
        storage_id = uuid4()
        user = Mock()
        storage = Mock()
        storage.id = storage_id

        mock_user_repository.find_by_keycloak_id.return_value = user
        mock_storage_repository.exists.return_value = True

        with pytest.raises(StorageAlreadyExistsError):
            storage_service.create_storage(storage, token_data)

    def test_delete_storage_success(
        self,
        storage_service,
        mock_session,
        mock_user_repository,
        mock_storage_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        storage_id = uuid4()
        user_id = uuid4()
        user = Mock()
        user.id = user_id
        storage = Mock()
        storage.id = storage_id

        mock_user_repository.find_by_keycloak_id.return_value = user
        mock_storage_repository.find_by_id.return_value = storage
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.ADMIN
        )

        storage_service.delete_storage(storage_id, token_data)

        mock_storage_repository.delete.assert_called_once_with(storage)
        mock_session.commit.assert_called_once()

    def test_delete_storage_not_found(
        self,
        storage_service,
        mock_user_repository,
        mock_storage_repository,
        token_data,
    ):
        storage_id = uuid4()
        user = Mock()

        mock_user_repository.find_by_keycloak_id.return_value = user
        mock_storage_repository.find_by_id.return_value = None

        with pytest.raises(StorageNotFoundError):
            storage_service.delete_storage(storage_id, token_data)

    def test_delete_storage_not_admin(
        self,
        storage_service,
        mock_user_repository,
        mock_storage_repository,
        mock_user_storage_access_repository,
        token_data,
    ):
        storage_id = uuid4()
        user_id = uuid4()
        user = Mock()
        user.id = user_id
        storage = Mock()
        storage.id = storage_id

        mock_user_repository.find_by_keycloak_id.return_value = user
        mock_storage_repository.find_by_id.return_value = storage
        mock_user_storage_access_repository.find_user_role.return_value = (
            UserRole.CONTRIBUTOR
        )

        with pytest.raises(AuthorizationError):
            storage_service.delete_storage(storage_id, token_data)
