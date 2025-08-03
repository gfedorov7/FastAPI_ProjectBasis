from typing import Generic, List

from pydantic import BaseModel, Field, ConfigDict

from src.types import ModelType


class PaginationParams(BaseModel):
    limit: int = Field(10, ge=0, le=100)
    offset: int = Field(0, ge=0)

class Pagination(BaseModel, Generic[ModelType]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    count: int
    items: List[ModelType]
