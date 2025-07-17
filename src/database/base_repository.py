from typing import Type, Sequence, Generic, Dict, Any
import logging

from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.types import ModelType, ID
from src.exceptions import NotFoundError

logger = logging.getLogger("app.database.base_repository")


class BaseRepository(Generic[ModelType]):
    def __init__(
            self,
            session: AsyncSession,
            model: Type[ModelType],
    ):
        self.session = session
        self.model = model

    async def get_by_id(self, id_: ID) -> ModelType:
        logger.debug(f"Fetching {self.model.__name__} by ID: {id_}")
        instance = await self._get_by_id(id_)
        self._check_exists_instance(instance, id_)
        logger.debug(f"Found {self.model.__name__} with ID: {id_}")
        return instance

    async def get_all(self, offset: int = 0, limit: int = 10) -> Sequence[ModelType]:
        logger.debug(f"Fetching all {self.model.__name__}s: offset={offset}, limit={limit}")
        stmt = select(self.model).offset(offset).limit(limit)
        return await self._get_all_results_from_query(stmt)

    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        logger.info(f"Creating new {self.model.__name__} with data: {obj_in}")
        instance = self._add_to_session(obj_in)
        await self._commit_and_refresh(instance)
        logger.info(f"Created {self.model.__name__} with ID: {getattr(instance, 'id', 'N/A')}")
        return instance

    async def update(self, id_: ID, obj_update: Dict[str, Any]) -> ModelType:
        logger.info(f"Updating {self.model.__name__} ID={id_} with data: {obj_update}")
        instance = await self.get_by_id(id_)
        instance = self._update_instance(instance, obj_update)
        await self._commit_and_refresh(instance)
        logger.info(f"Updated {self.model.__name__} ID={id_}")
        return instance

    async def delete(self, id_: ID) -> None:
        logger.info(f"Deleting {self.model.__name__} with ID: {id_}")
        instance = await self.get_by_id(id_)
        await self.session.delete(instance)
        await self.session.commit()
        logger.info(f"Deleted {self.model.__name__} with ID: {id_}")

    async def exists(self, *conditions) -> bool:
        logger.debug(f"Checking existence of {self.model.__name__} with conditions: {conditions}")
        stmt = select(self.model).where(*conditions).limit(1)
        instances = await self._get_all_results_from_query(stmt)
        exists = self._condition_for_check_exists_instances(instances)
        logger.debug(f"Existence check result for {self.model.__name__}: {exists}")
        return exists

    async def count(self, *conditions) -> int:
        logger.debug(f"Counting {self.model.__name__}s with conditions: {conditions}")
        stmt = select(func.count()).select_from(self.model).where(*conditions)
        result = await self.session.execute(stmt)
        count = result.scalar_one_or_none() or 0
        logger.debug(f"Count result for {self.model.__name__}: {count}")
        return count

    async def get_by_conditions(self, *conditions) -> Sequence[ModelType]:
        logger.debug(f"Getting {self.model.__name__}s with conditions: {conditions}")
        stmt = select(self.model).where(*conditions)
        return await self._get_all_results_from_query(stmt)

    async def _get_by_id(self, id_: ID) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id_)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def _check_exists_instance(self, instance: ModelType | None, id_: ID) -> None:
        if instance is None:
            logger.warning(f"{self.model.__name__} not found with ID {id_}")
            raise NotFoundError(self.model.__name__, id_)

    def _add_to_session(self, obj_in: Dict[str, Any]) -> ModelType:
        instance = self.model(**obj_in)
        self.session.add(instance)
        return instance

    async def _commit_and_refresh(self, instance: ModelType | None) -> None:
        await self.session.commit()
        if instance:
            await self.session.refresh(instance)

    @staticmethod
    def _update_instance(instance: ModelType, obj_update: Dict[str, Any]) -> ModelType:
        for key, value in obj_update.items():
            if value is not None:
                setattr(instance, key, value)
        return instance

    @staticmethod
    def _condition_for_check_exists_instances(instances: Sequence[ModelType]) -> bool:
        return len(instances) != 0

    async def _get_all_results_from_query(self, stmt: Select) -> Sequence[ModelType]:
        result = await self.session.execute(stmt)
        return result.scalars().all()
