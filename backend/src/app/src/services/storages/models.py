from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.join_tables.user_storage import (
    user_storage_access,
)

if TYPE_CHECKING:
    from backend.src.app.src.services.sensors.models import SensorModel
    from backend.src.app.src.services.users.models import UserModel


class StorageModel(BaseModel):
    __tablename__ = "Storage"

    name: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    password_salt: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    accessing_users: Mapped[list["UserModel"]] = relationship(
        secondary=user_storage_access, back_populates="accessed_storages"
    )
    sensors: Mapped[list["SensorModel"]] = relationship(
        back_populates="storage"
    )
