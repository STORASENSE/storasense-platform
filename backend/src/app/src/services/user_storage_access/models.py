from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.enums import UserRole

if TYPE_CHECKING:
    from backend.src.app.src.services.storages.models import StorageModel
    from backend.src.app.src.services.users.models import UserModel


class UserStorageAccessModel(BaseModel):
    """
    This class represents the junktion table for the many-to-many relationship between
    the `User` and the `Storage` tables. It also contains the `UserRole` that can be used
    for authorization purposes.
    """

    __tablename__ = "UserStorageAccess"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("User.id"), primary_key=True
    )
    storage_id: Mapped[UUID] = mapped_column(
        ForeignKey("Storage.id"), primary_key=True
    )
    user: Mapped["UserModel"] = relationship(
        back_populates="storage_associations"
    )
    storage: Mapped["StorageModel"] = relationship(
        back_populates="user_associations"
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.CONTRIBUTOR
    )
