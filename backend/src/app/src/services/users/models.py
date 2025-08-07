from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.join_tables.user_storage import (
    user_storage_access,
)

if TYPE_CHECKING:
    from backend.src.app.src.services.storages.models import StorageModel


class UserModel(BaseModel):
    __tablename__ = "User"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    provider_sub: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    name: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default="user"
    )

    description: Mapped[Optional[str]] = mapped_column()
    accessed_storages: Mapped[list["StorageModel"]] = relationship(
        secondary=user_storage_access, back_populates="accessing_users"
    )
