from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.join_tables.user_storage import (
    UserStorageAccess,
)

if TYPE_CHECKING:
    from backend.src.app.src.services.sensors.models import SensorModel
    from backend.src.app.src.services.users.models import UserModel


class StorageModel(BaseModel):
    __tablename__ = "Storage"

    name: Mapped[str] = mapped_column(unique=False)
    description: Mapped[Optional[str]] = mapped_column()

    user_associations: Mapped[list[UserStorageAccess]] = relationship(
        back_populates="storage", cascade="all, delete-orphan"
    )
    accessing_users: Mapped[list["UserModel"]] = relationship(
        secondary=UserStorageAccess.__table__,
        back_populates="accessed_storages",
    )

    sensors: Mapped[list["SensorModel"]] = relationship(
        back_populates="storage"
    )
