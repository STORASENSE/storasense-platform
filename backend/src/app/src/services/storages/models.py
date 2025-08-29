from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel

if TYPE_CHECKING:
    from backend.src.app.src.services.sensors.models import SensorModel
    from backend.src.app.src.services.users.models import UserModel
    from backend.src.app.src.services.user_storage_access.models import (
        UserStorageAccessModel,
    )


class StorageModel(BaseModel):
    __tablename__ = "Storage"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]] = mapped_column()

    user_associations: Mapped[list["UserStorageAccessModel"]] = relationship(
        back_populates="storage", cascade="all, delete-orphan"
    )
    accessing_users: Mapped[list["UserModel"]] = relationship(
        secondary="UserStorageAccess",
        back_populates="accessed_storages",
    )

    sensors: Mapped[list["SensorModel"]] = relationship(
        back_populates="storage"
    )
