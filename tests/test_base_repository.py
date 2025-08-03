import random

import pytest
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped

from src.database.base import Base
from src.database.base_repository import BaseRepository
from src.exceptions import NotFoundRecord


class PersonTestModel(Base):
    name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()

    __table_args__ = (
        CheckConstraint('age >= 0 AND age <= 120', name="check_age_range"),
    )

@pytest.fixture
def repo(session: AsyncSession) -> BaseRepository[PersonTestModel]:
    return BaseRepository(session, PersonTestModel)

async def add_new_person(repo: BaseRepository, session: AsyncSession) -> PersonTestModel:
    obj_in = {"name": "test", "age": 10}

    obj = await repo.create(obj_in)
    await session.commit()

    return obj

@pytest.mark.asyncio
async def test_create(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    assert obj.name == "test"
    assert obj.age == 10
    assert obj.id is not None

@pytest.mark.asyncio
async def test_get_by_id(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    obj = await repo.get_by_id(obj.id)
    assert obj.name == "test"
    assert obj.age == 10

@pytest.mark.asyncio
async def test_get_by_id_not_found(repo: BaseRepository):
    unknown_id = random.randint(99999, 999999999)

    with pytest.raises(NotFoundRecord):
        await repo.get_by_id(unknown_id)

@pytest.mark.asyncio
async def test_get_all(repo: BaseRepository):
    objs = await repo.get_all()

    assert type(objs) is list

@pytest.mark.asyncio
async def test_update(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    new_obj = await repo.update(obj.id, {"name": "updated_test"})

    assert new_obj.name == "updated_test"
    assert new_obj.age == 10

@pytest.mark.asyncio
async def test_delete(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    await repo.delete(obj.id)

    with pytest.raises(NotFoundRecord):
        await repo.get_by_id(obj.id)

@pytest.mark.asyncio
async def test_exists(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    is_exists = await repo.exists(repo.model.name == obj.name)

    assert is_exists is True

@pytest.mark.asyncio
async def test_exists_not_found(repo: BaseRepository):
    is_exists = await repo.exists(repo.model.name == "")

    assert is_exists is False

@pytest.mark.asyncio
async def test_count(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    count = await repo.count(repo.model.name == obj.name)

    assert count == 6 # 6 because use add_new_person 6 times before

@pytest.mark.asyncio
async def test_count_not_found(repo: BaseRepository):
    count = await repo.count(repo.model.name == "")

    assert count == 0

@pytest.mark.asyncio
async def test_get_by_condition(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    found = await repo.get_by_conditions(repo.model.name == obj.name)

    assert obj in found

@pytest.mark.asyncio
async def test_get_by_condition_limit_zero(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    found = await repo.get_by_conditions(repo.model.name == obj.name, offset=0, limit=0)

    assert len(found) == 0

@pytest.mark.asyncio
async def test_get_one_by_condition(repo: BaseRepository, session: AsyncSession):
    obj = await add_new_person(repo, session)

    found = await repo.get_one_by_conditions(repo.model.name == obj.name)

    assert found.id is not None

@pytest.mark.asyncio
async def test_get_one_by_condition_not_found(repo: BaseRepository):
    result = await repo.get_one_by_conditions(repo.model.name == "")

    assert result is None