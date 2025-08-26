from uuid import UUID
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.src.app.src.services.alarms.models import AlarmModel
from backend.src.app.src.services.alarms.repository import (
    AlarmRepository,
    inject_alarm_repository,
)
from backend.src.app.src.services.storages.repository import (
    StorageRepository,
    inject_storage_repository,
)
from backend.src.app.src.shared.database.engine import open_session
from backend.src.app.src.shared.database.pagination import PageRequest, Page


class AlarmService:
    def __init__(
        self,
        session: Session,
        alarm_repository: AlarmRepository,
        storage_repository: StorageRepository,
    ):
        self._session = session
        self._alarm_repository = alarm_repository
        self._storage_repository = storage_repository

    def find_alarm_by_id(self, alarm_id: UUID) -> Optional[AlarmModel]:
        """Finds an alarm by its ID."""
        return self._alarm_repository.find_by_id(alarm_id)

    def find_alarms_by_storage_id(
        self, storage_id: UUID, page_request: PageRequest
    ) -> Page[AlarmModel]:
        """
        Returns all alarms for a given storage (linked via Sensor → Measurements),
        sorted by alarm timestamp in descending order and paginated.
        Note: For performance reasons, a raw SQL query is used.

        :param storage_id: The ID of the storage to get alarms for.
        :param page_request: The pagination request.
        :return: A page containing the requested alarm data.
        :raises ValueError: If the storage with the given ID does not exist.
        """
        # Verify storage exists first
        storage = self._storage_repository.find_by_id(storage_id)
        if not storage:
            raise ValueError(f"Storage with ID {storage_id} does not exist.")

        return self._alarm_repository.find_alarms_by_storage_id(
            storage_id, page_request
        )


def inject_alarm_service(
    session: Session = Depends(open_session),
    alarm_repository: AlarmRepository = Depends(inject_alarm_repository),
    storage_repository: StorageRepository = Depends(inject_storage_repository),
) -> AlarmService:
    return AlarmService(session, alarm_repository, storage_repository)
