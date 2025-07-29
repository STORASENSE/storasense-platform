"""
This script drops all tables from the connected database (if they exist)
and then creates all tables.

Note that this script is for development only, and future usage should
occur via a proper database migration tool, such as Alembic.
"""

from backend.src.app.src.shared.database.base_model import BaseModel
from backend.src.app.src.shared.database.engine import db_engine

if __name__ == "__main__":
    BaseModel.metadata.drop_all(db_engine)
    BaseModel.metadata.create_all(db_engine)
