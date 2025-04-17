from random import randint
from datetime import datetime

import pytest
from fastapi import status
from fastapi.exceptions import HTTPException

from app.reservations.dao import ReservationDAO
from app.reservations.models import Reservation
from tests.conftest import fake


class TestReservationsServices:

    @pytest.mark.asyncio(loop_scope="session")
    async def test_successful_add_reservation(self, existing_table):
        """Тестируем успешное создание бронирования."""
        service = ReservationDAO()
        data = {
            'customer_name': fake.name(),
            'reservation_time': datetime.fromisoformat(fake.iso8601()),
            'duration_minutes': randint(1, 20),
            'table_id': existing_table.id
        }

        response = await service.add_reservation(**data)

        assert isinstance(response, Reservation)
        assert response.customer_name == data['customer_name']
        assert response.duration_minutes == data['duration_minutes']

    @pytest.mark.asyncio(loop_scope="session")
    async def test_conflicting_times(self, existing_reservation):
        """Проверяем обработку конфликта по времени."""
        service = ReservationDAO()
        data = {
            'customer_name': fake.name(),
            'reservation_time': existing_reservation.reservation_time,
            'duration_minutes': 60,
            'table_id': existing_reservation.table_id
        }

        with pytest.raises(HTTPException) as exc_info:
            await service.add_reservation(**data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            exc_info.value.detail ==
            "Выбранное время уже занято другим бронированием"
        )
