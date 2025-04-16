from datetime import datetime

from pydantic import BaseModel, Field


class BaseReservationShema(BaseModel):
    """
    Базовая схема бронирования.

    Attributes:
        customer_name (str): Имя клиента.
        table_id (int): Id столика.
        reservation_time (datetime): Время начала бронирования.
        duration_minutes (int): Продолжительность бронирования
        в минутах (минимум 10 минут).
    """
    customer_name: str = Field(..., description="Имя клиента")
    table_id: int = Field(..., description="Id столика")
    reservation_time: datetime = Field(..., description="Дата бронирования")
    duration_minutes: int = Field(..., ge=10, description="Время бронирования")


class GetReservationSchema(BaseReservationShema):
    """
    Схема для получения данных о бронировании.

    Attributes:
        id (int): Уникальный идентификатор бронирования.
    """
    id: int


class AddReservationSchema(BaseReservationShema):
    """
    Схема для добавления нового бронирования.
    """
    pass
