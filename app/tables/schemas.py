from pydantic import BaseModel, Field


class BaseTableShema(BaseModel):
    """
    Базовая схема стола.

    Attributes:
        name (str): Название столика.
        seats (int): Количество мест за столом (не менее одного места).
        location (str): Место расположения столика.
    """
    name: str = Field(..., description="Название столика")
    seats: int = Field(..., ge=1, description="Количество мест")
    location: str = Field(..., description="Место расположения")


class GetTableSchema(BaseTableShema):
    """
    Схема для представления информации о столе при получении данных.

    Attributes:
        id (int): Уникальный идентификатор стола.
    """
    id: int


class AddTableSchema(BaseTableShema):
    """
    Схема для добавления нового стола.
    """
    pass
