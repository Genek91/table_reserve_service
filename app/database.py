from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncAttrs)
from sqlalchemy.orm import (DeclarativeBase, declared_attr, Mapped,
                            mapped_column)

from app.config import get_db_url


DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей приложения.
    """
    __abstract__ = True

    # Автоматическое присвоение имени таблицы исходя из имени класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Общие поля для всех наследуемых классов
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
