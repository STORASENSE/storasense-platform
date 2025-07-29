from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.join_tables.user_storage import (
    user_storage_access,
)

if TYPE_CHECKING:
    from backend.src.app.src.services.storages.models import StorageModel


class UserModel(BaseModel):
    __tablename__ = "User"

    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    password_salt: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    accessed_storages: Mapped[list["StorageModel"]] = relationship(
        user_storage_access, back_populates="accessing_users"
    )
