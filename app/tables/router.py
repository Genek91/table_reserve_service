from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.tables.dao import TableDAO
from app.tables.schemas import GetTableSchema, AddTableSchema


table_router = APIRouter(prefix='/tables', tags=['Столики'])


@table_router.get(
        "/", summary="Список всех столиков"
    )
async def get_all_tables() -> list[GetTableSchema]:
    return await TableDAO.get_all()


@table_router.post("/", summary="Cоздать новый столик")
async def create_table(table: AddTableSchema) -> GetTableSchema:
    try:
        return await TableDAO.add(**table.model_dump())
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Столик с таким названием уже существует"
        )


@table_router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Удалить столик"
    )
async def delete_table(id: int) -> None:
    try:
        return await TableDAO.delete_by_id(id)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при удалении столика"
        )
