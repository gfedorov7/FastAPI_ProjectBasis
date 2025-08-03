from typing import Generic, Type, Sequence, Dict, Any

from sqlalchemy import select, Result, func, exists, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.types import ID, ModelType
from src.exceptions import NotFoundRecord


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, id_: ID) -> ModelType:
        stmt = select(self.model).where(self.model.id == id_)
        record_or_none: ModelType = await self._get_scalar(stmt=stmt)

        self._check_exists_element(record_or_none)

        return record_or_none

    async def get_all(self, limit: int = 10, offset: int = 0) -> Sequence[ModelType]:
        stmt = select(self.model).limit(limit).offset(offset)
        return await self._get_scalars(stmt=stmt)

    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        obj = self.model(**obj_in)
        self.session.add(obj)
        return obj

    async def update(self, id_: ID, obj_in: Dict[str, Any]) -> ModelType:
        instance = await self.get_by_id(id_)
        return self._update_instance(instance, obj_in)

    async def delete(self, id_: ID) -> None:
        obj = await self.get_by_id(id_)
        await self.session.delete(obj)

    async def exists(self, *conditions) -> bool:
        stmt = select(exists().where(*conditions))
        return bool(await self._get_scalar(stmt=stmt))

    async def count(self, *conditions) -> int:
        stmt = select(func.count()).where(*conditions)
        return await self._get_scalar(stmt=stmt) or 0

    async def get_by_conditions(self, *conditions, offset: int = 0, limit: int = 10) -> Sequence[ModelType]:
        stmt = select(self.model).where(*conditions).offset(offset).limit(limit)
        return await self._get_scalars(stmt=stmt)

    async def get_one_by_conditions(self, *conditions):
        records = await self.get_by_conditions(*conditions, offset=0, limit=1)
        self._check_exists_element(records)
        return records[0]

    async def _get_scalar(self, stmt: Select) -> Any:
        result: Result = await self.session.execute(stmt)
        return result.scalar()

    def _check_exists_element(self, record: ModelType | Sequence[ModelType] | Sequence[None] | None) -> None:
        if not record:
            raise NotFoundRecord(self.model.__name__)

    async def _get_scalars(self, stmt: Select):
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def _update_instance(instance: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        for key, value in obj_in.items():
            setattr(instance, key, value)
        return instance