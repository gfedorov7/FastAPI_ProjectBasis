from typing import TypeVar
import uuid

from sqlalchemy.orm import Mapped

from src.database.base import Base


ModelType = TypeVar("ModelType", bound=Base)
ID = TypeVar("ID", uuid.UUID, int, Mapped)
