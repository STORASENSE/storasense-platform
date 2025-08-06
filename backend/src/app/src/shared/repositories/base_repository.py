from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.pagination import (
    Page,
    PageRequest,
)


class BaseRepository[T: BaseModel, ID](ABC):
    """
    This class is the base of every repository. It provides common methods for CRUD operations.
    Due to language limitations, implementing classes need to implement the `find_by_id` and
    `find_all` methods.
    """

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def find_by_id(self, object_id: ID) -> Optional[T]:
        """
        Finds an entity by their primary key.

        :param object_id: The primary key to look for.
        :return: The entity if found, otherwise `None`
        """
        pass

    def find_all(self, page_request: [PageRequest]) -> Page[T]:
        """
        Finds all entities and paginates the result.

        :param page_request: The pagination request.
        :return: The requested page.
        """
        pass

    def create(self, obj: T):
        """
        Inserts the given entity into the database. The primary key should not be set manually,
        as it is automatically assigned to the given entity after flushing the session to the
        database.

        :param obj: The entity to insert into the database.
        """
        self.session.add(obj)
        self.session.flush()

    def delete(self, obj: T):
        """
        Deletes the given entity from the database. The given object is assumed to be persisted
        in the database. This method only flushes the deletion to the database, which means the
        entity is not yet removed from the database by calling this method. To do so, commit the
        session.

        :param obj: The entity to delete from the database.
        """
        self.session.delete(obj)
        self.session.flush()

    def delete_by_id(self, object_id: ID):
        """
        Deletes the entity whose primary key corresponds to the given parameter from the database.
        The entity is assumed to be persisted in the database. This method only flushes the deletion
        to the database, which means the entity is not yet removed from the database by calling this
        method. To do so, commit the session.

        :param object_id: The entity's primary key.
        """
        obj = self.find_by_id(object_id)
        self.delete(obj)

    def exists(self, object_id: ID) -> bool:
        """
        Checks if an entity with the given primary key exists in the database.
        The entity needs not to be persisted in order to be found, as long as the session
        was flushed.

        :param object_id: The entity's primary key.
        :return: Whether an entity with the given primary key exists.
        """
        return self.find_by_id(object_id) is not None
