from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)

            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def get_all_by_filter(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)

            return result.scalars().all()

    @classmethod
    async def add(cls, **kwargs):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**kwargs)
                session.add(new_instance)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

                return new_instance

    @classmethod
    async def delete_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            to_delete = result.scalar_one_or_none()

            if not to_delete:
                return None

            await session.execute(
                delete(cls.model).filter_by(id=id)
            )
            await session.commit()
