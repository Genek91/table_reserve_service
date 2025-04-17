import pytest
from fastapi import status

from tests.conftest import fake


class TestTablesAPI:
    """
    Набор тестов для проверки функционала API управления столиками.
    """

    @pytest.mark.asyncio(loop_scope="session")
    async def test_create_table(self, client):
        """
        Тестирует создание нового столика.
        """
        data = {
            "name": fake.name(),
            "seats": fake.random_int(1, 20),
            "location": fake.word()
        }

        response = await client.post("/tables/", json=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["seats"] == data["seats"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_tables(self, client, existing_table):
        """
        Тестирует получение списка всех столиков.
        """
        response = await client.get("/tables/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["location"] == existing_table.location

    @pytest.mark.asyncio(loop_scope="session")
    async def test_del_table(self, client, existing_table):
        """
        Тестирует удаление конкретного столика.
        """
        response = await client.delete(f"/tables/{existing_table.id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT
