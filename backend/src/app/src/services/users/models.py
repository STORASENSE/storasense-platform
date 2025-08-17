from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.join_tables.user_storage import (
    UserStorageAccess,
)

if TYPE_CHECKING:
    from backend.src.app.src.services.storages.models import StorageModel


class UserModel(BaseModel):
    __tablename__ = "User"

    keycloak_id: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=True
    )  # Allow null for email to support technical users
    name: Mapped[str] = mapped_column(
        String(255), unique=False, index=False, nullable=True
    )  # Allow null for name to support technical users

    storage_associations: Mapped[list[UserStorageAccess]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    accessed_storages: Mapped[list["StorageModel"]] = relationship(
        secondary=UserStorageAccess.__table__, back_populates="accessing_users"
    )
