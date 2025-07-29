from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.pagination import (
    Page,
    PageRequest,
)


class BaseRepository[T: BaseModel, ID](ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def find_by_id(self, object_id: ID) -> Optional[T]:
        pass

    @abstractmethod
    def find_all(self, page_request: [PageRequest]) -> Page[T]:
        pass

    def create(self, obj: T):
        self.session.add(obj)
        self.session.flush()

    def delete(self, obj: T):
        self.session.delete(obj)
        self.session.flush()

    def delete_by_id(self, object_id: ID):
        obj = self.find_by_id(object_id)
        self.delete(obj)

    def exists(self, object_id: ID) -> bool:
        return self.find_by_id(object_id) is not None
