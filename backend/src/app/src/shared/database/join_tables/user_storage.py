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
"""
This object represents the junktion table for the many-to-many relationship between
the `User` and the `Storage` tables. It also contains the `UserRole` that can be used
for authorization purposes.
"""
