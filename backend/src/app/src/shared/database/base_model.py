from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """
    This class is the base for any database model. According to the planned architecture,
    each table has a primary key `id` of type `UUID`, which has been adopted in this class.

    Attributes:
        id (UUID): The model's primary key.
    """

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
