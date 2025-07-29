from sqlalchemy import Column, Enum, ForeignKey, Table

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.enums import UserRole

user_storage_access = Table(
    "UserStorageAccess",
    BaseModel.metadata,
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("storage_id", ForeignKey("Storage.id"), primary_key=True),
    Column("user_role", Enum(UserRole)),
)
