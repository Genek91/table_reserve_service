from app.dao import BaseDAO
from app.tables.models import Table


class TableDAO(BaseDAO):
    """
    Data Access Object для работы с моделью Table.
    """
    model = Table
