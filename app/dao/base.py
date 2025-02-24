
from app.database import ses_mark, async_session_maker, engine

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    # Найти строчку по id
    @classmethod
    async def find_by_id(cls, model_if: int):
        async with async_session_maker() as session:
            # SELECT * FROM cls.model
            # WHERE id=model_if
            query = select(cls.model).filter_by(id=model_if)
            result = await session.execute(query)

            # Вывести одно значение или None
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            # SELECT * FROM cls.model
            # WHERE любой фильтр
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)

            # Вывести одно значение или None
            return result.scalar_one_or_none()
            #return result.scalars().all()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            # SELECT * FROM cls.model
            # WHERE любой фильтр
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            # Вывести кортеж
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with ses_mark() as session:

            query = insert(cls.model).values(**data)

            await session.execute(query)


    @classmethod
    async def add2(cls, **data):
        async with AsyncSession(engine) as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

