from datetime import timedelta, datetime

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.dao import BaseDAO
from app.database import async_session_maker
from app.reservations.models import Reservation


class ReservationDAO(BaseDAO):
    model = Reservation

    @classmethod
    async def add_reservation(
        cls, customer_name: str, reservation_time: datetime,
        duration_minutes: int, table_id: int
    ):
        if reservation_time.tzinfo is not None:
            reservation_time = reservation_time.replace(tzinfo=None)

        end_time = reservation_time + timedelta(minutes=duration_minutes)

        async with async_session_maker() as session:
            async with session.begin():
                existing_reservations = await cls.get_all_by_filter(
                    table_id=table_id
                )

                for reservation in existing_reservations:
                    existing_end_time = reservation.reservation_time + timedelta(
                        minutes=reservation.duration_minutes
                    )

                    if (reservation_time < existing_end_time and end_time > reservation.reservation_time):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=(
                                "Выбранное время уже занято другим "
                                "бронированием"
                            )
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
