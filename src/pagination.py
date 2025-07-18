from typing import Generic, TypeVar, List

from pydantic import BaseModel


T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
