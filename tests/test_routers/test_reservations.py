from random import randint

import pytest
from fastapi import status

from tests.conftest import fake


class TestReservationsAPI:
    """
    Набор тестов для проверки функционала API бронирования.
    """

    @pytest.mark.asyncio(loop_scope="session")
    async def test_create_reservation(self, client, existing_table):
        """
        Тестирует создание нового бронирования.
        """
        data = {
            "customer_name": fake.name(),
            "table_id": existing_table.id,
            "reservation_time": str(fake.iso8601()),
            "duration_minutes": randint(10, 99)
        }

        response = await client.post("/reservations/", json=data)

        assert response.status_code == status.HTTP_200_OK
        assert (
            response.json()["customer_name"] == data["customer_name"]
        )

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_reservations(self, client, existing_reservation):
        """
        Тестирует получение всех бронирований.
        """
        response = await client.get("/reservations/")

        assert response.status_code == status.HTTP_200_OK
        assert (
            response.json()[0]["reservation_time"] ==
            existing_reservation.reservation_time.isoformat()
        )

    @pytest.mark.asyncio(loop_scope="session")
    async def test_del_reservation(self, client, existing_reservation):
        """
        Тестирует удаление конкретного бронирования.
        """
        response = await client.delete(
            f"/reservations/{existing_reservation.id}"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
