from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker


class BaseDAO:
    """
    Базовый класс DAO (Data Access Object), предоставляющий методы
    для взаимодействия с базой данных.

    Attributes:
        model: Класс модели, используемый для CRUD операций.
    """

    model = None

    @classmethod
    async def get_all(cls) -> list:
        """
        Получение всех записей указанной модели.

        Returns:
            Список экземпляров модели.
        """
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)

            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id: int):
        """
        Получение записи по её идентификатору.

        Args:
            id: Идентификатор записи.

        Returns:
            Экземпляр модели или None, если запись не найдена.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def get_all_by_filter(cls, **kwargs) -> list:
        """
        Получение всех записей, соответствующих заданному фильтру.

        Args:
            kwargs: Параметры фильтра.

        Returns:
            Список экземпляров модели.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)

            return result.scalars().all()

    @classmethod
    async def add(cls, **kwargs):
        """
        Добавление новой записи в базу данных.

        Args:
            kwargs: Параметры для инициализации экземпляра модели.

        Raises:
            SQLAlchemyError: Если произошла ошибка при выполнении транзакции.

        Returns:
            Новый экземпляр модели.
        """
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
    async def delete_by_id(cls, id: int) -> None:
        """
        Удаление записи по её идентификатору.

        Args:
            id: Идентификатор записи.

        Returns:
            None
        """
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
