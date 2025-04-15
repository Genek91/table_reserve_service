from app.dao import BaseDAO
from app.tables.models import Table


class TableDAO(BaseDAO):
    model = Table
