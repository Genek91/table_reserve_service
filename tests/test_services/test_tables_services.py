from random import randint

import pytest

from app.tables.models import Table
from app.tables.dao import TableDAO
from tests.conftest import fake


class TestTablesServices:

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_tables(self):
        """Тестирование получения списка столов"""
        tales = await TableDAO.get_all()

        assert isinstance(tales, list)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_table_by_id(self, existing_table):
        """Тестирование получения конкретного стола по ID"""
        retrieved_table = await TableDAO.get_by_id(existing_table.id)

        assert retrieved_table is not None
        assert retrieved_table.id == existing_table.id

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_filtered_tables(self, existing_table):
        """Тестирование выборки по фильтрам"""
        filtered_tables = await TableDAO.get_all_by_filter(
            id=existing_table.id
        )

        assert len(filtered_tables) > 0
        for table in filtered_tables:
            assert table.id == existing_table.id

    @pytest.mark.asyncio(loop_scope="session")
    async def test_add_new_table(self):
        """Тестирование добавления нового стола"""
        new_table_data = {
            "name": fake.name(),
            "seats": randint(1, 10),
            "location": fake.word()
        }

        added_table = await TableDAO.add(**new_table_data)

        assert isinstance(added_table, Table)
        assert added_table.name == new_table_data["name"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_delete_existing_table(self, existing_table):
        """Тестирование удаления существующего стола"""
        await TableDAO.delete_by_id(existing_table.id)
        table = await TableDAO.get_by_id(existing_table.id)

        assert table is None
