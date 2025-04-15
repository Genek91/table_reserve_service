from fastapi import FastAPI

from app.config import settings
from app.tables.router import table_router
from app.reservations.router import reservation_router

app = FastAPI(title=settings.app_title, description=settings.description)
app.include_router(table_router)
app.include_router(reservation_router)
