import pytest
from unittest.mock import Mock, patch
from uuid import uuid4

from backend.src.app.src.services.storages.repository import StorageRepository
from backend.src.app.src.services.storages.models import StorageModel
from backend.src.app.src.shared.database.pagination import PageRequest, Page


class TestStorageRepository:
    @pytest.fixture
    def mock_session(self):
        mock_session = Mock()
        mock_session.query.return_value = mock_session
        mock_session.get.return_value = None
        mock_session.where.return_value = mock_session
        mock_session.one_or_none.return_value = None
        mock_session.join.return_value = mock_session
        mock_session.filter_by.return_value = mock_session
        mock_session.all.return_value = []
        return mock_session

    @pytest.fixture
    def storage_repository(self, mock_session):
        return StorageRepository(mock_session)

    def test_find_by_id_success(self, storage_repository, mock_session):
        storage_id = uuid4()
        expected_storage = Mock(spec=StorageModel)

        mock_session.get.return_value = expected_storage

        result = storage_repository.find_by_id(storage_id)

        assert result == expected_storage
        mock_session.get.assert_called_once_with(storage_id)

    def test_find_by_id_not_found(self, storage_repository, mock_session):
        storage_id = uuid4()

        mock_session.get.return_value = None

        result = storage_repository.find_by_id(storage_id)

        assert result is None

    @patch("backend.src.app.src.services.storages.repository.paginate")
    def test_find_all(self, mock_paginate, storage_repository, mock_session):
        page_request = PageRequest(page_number=1, page_size=10)
        expected_page = Page(
            items=[], page_size=10, page_number=1, total_pages=0
        )

        mock_paginate.return_value = expected_page

        result = storage_repository.find_all(page_request)

        assert result == expected_page
        mock_paginate.assert_called_once()

    def test_find_by_name_success(self, storage_repository, mock_session):
        name = "Test Storage"
        expected_storage = Mock(spec=StorageModel)

        mock_session.one_or_none.return_value = expected_storage

        result = storage_repository.find_by_name(name)

        assert result == expected_storage

    def test_find_by_name_not_found(self, storage_repository, mock_session):
        name = "Nonexistent Storage"

        mock_session.one_or_none.return_value = None

        result = storage_repository.find_by_name(name)

        assert result is None

    def test_find_all_by_user_id(self, storage_repository, mock_session):
        user_id = uuid4()
        expected_storages = [Mock(spec=StorageModel), Mock(spec=StorageModel)]

        mock_session.all.return_value = expected_storages

        result = storage_repository.find_all_by_user_id(user_id)

        assert result == expected_storages

    def test_exists_by_name_true(self, storage_repository, mock_session):
        name = "Existing Storage"

        mock_session.one_or_none.return_value = Mock(spec=StorageModel)

        result = storage_repository.exists_by_name(name)

        assert result is True

    def test_exists_by_name_false(self, storage_repository, mock_session):
        name = "Nonexistent Storage"

        mock_session.one_or_none.return_value = None

        result = storage_repository.exists_by_name(name)

        assert result is False
