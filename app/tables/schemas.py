from pydantic import BaseModel, Field


class BaseTableShema(BaseModel):
    name: str = Field(..., description="Название столика")
    seats: int = Field(..., ge=1, description="Количество мест")
    location: str = Field(..., description="Место расположения")


class GetTableSchema(BaseTableShema):
    id: int


class AddTableSchema(BaseTableShema):
    pass
