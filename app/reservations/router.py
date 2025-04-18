from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.reservations.dao import ReservationDAO
from app.tables.dao import TableDAO
from app.reservations.schemas import GetReservationSchema, AddReservationSchema


reservation_router = APIRouter(prefix='/reservations', tags=['Брони'])


@reservation_router.get(
        "/", summary="Список всех броней"
    )
async def get_all_reservations() -> list[GetReservationSchema]:
    """
    Получение списка всех забронированных столиков.

    Returns:
        list[GetReservationSchema]: Список объектов бронирований.
    """
    return await ReservationDAO.get_all()


@reservation_router.post("/", summary="Cоздать новую бронь")
async def create_reservation(
    reservation: AddReservationSchema
) -> GetReservationSchema:
    """
    Создание нового бронирования столика.

    Args:
        reservation (AddReservationSchema): Данные для создания бронирования.

    Returns:
        GetReservationSchema: Объект созданного бронирования.

    Raises:
        HTTPException: Если выбранный столик не найден или возникла ошибка
        при сохранении.
    """
    chek_table = await TableDAO.get_by_id(reservation.table_id)

    if chek_table is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Невозможно создать бронь: "
                "выбранного столика не существует"
            )
        )

    try:
        return await ReservationDAO.add_reservation(**reservation.model_dump())
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании брони {e}"
        )


@reservation_router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Удалить бронь"
    )
async def delete_reservation(id: int) -> None:
    """
    Удаляет существующую бронь по указанному ID.

    Args:
        id (int): Идентификатор бронирования.

    Raises:
        HTTPException: Если возникла ошибка при удалении брони.
    """
    try:
        return await ReservationDAO.delete_by_id(id)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при удалении брони"
        )
