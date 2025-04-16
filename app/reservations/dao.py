from datetime import timedelta, datetime

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, select, cast, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.types import Interval

from app.dao import BaseDAO
from app.database import async_session_maker
from app.reservations.models import Reservation


class ReservationDAO(BaseDAO):
    """
    Data Access Object для работы с моделями бронирования.
    """
    model = Reservation

    @classmethod
    async def add_reservation(
        cls, customer_name: str, reservation_time: datetime,
        duration_minutes: int, table_id: int
    ):
        """
        Проверка наличия конфликтов по времени и создание нового бронирования.

        Args:
            customer_name (str): Имя клиента.
            reservation_time (datetime): Время начала бронирования.
            duration_minutes (int): Продолжительность бронирования в минутах.
            table_id (int): Идентификатор столика.

        Raises:
            HTTPException: Если возник конфликт по времени с существующими
            бронированиями.
            SQLAlchemyError: Если возникла ошибка при работе с базой данных.

        Returns:
            Reservation: Объект созданного бронирования.
        """
        if reservation_time.tzinfo is not None:
            reservation_time = reservation_time.replace(tzinfo=None)

        end_time = reservation_time + timedelta(minutes=duration_minutes)

        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    select(Reservation).where(
                        and_(
                            Reservation.table_id == table_id,
                            Reservation.reservation_time < end_time,
                            Reservation.reservation_time + cast(
                                text(f"interval '{duration_minutes} minutes'"),
                                Interval
                            ) > reservation_time
                        )
                    )
                )

            result = await session.execute(query)
            conflicting_reservations = result.scalars().first()

            if conflicting_reservations:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Выбранное время уже занято другим бронированием"
                )

            new_reservation = Reservation(
                customer_name=customer_name,
                reservation_time=reservation_time,
                duration_minutes=duration_minutes,
                table_id=table_id
            )
            session.add(new_reservation)

            try:
                await session.commit()
                return new_reservation
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
