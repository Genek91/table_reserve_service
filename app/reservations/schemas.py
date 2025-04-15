from datetime import datetime

from pydantic import BaseModel, Field


class BaseReservationShema(BaseModel):
    customer_name: str = Field(..., description="Имя клиента")
    table_id: int = Field(..., description="Id столика")
    reservation_time: datetime = Field(..., description="Дата бронирования")
    duration_minutes: int = Field(..., ge=10, description="Время бронирования")


class GetReservationSchema(BaseReservationShema):
    id: int


class AddReservationSchema(BaseReservationShema):
    pass
