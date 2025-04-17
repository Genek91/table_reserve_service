from datetime import datetime
from random import randint

from httpx import ASGITransport, AsyncClient
from faker import Faker
import pytest_asyncio

from app.database import async_session_maker
from app.main import app
from app.tables.models import Table
from app.reservations.models import Reservation


fake = Faker()


@pytest_asyncio.fixture(scope="function", loop_scope="session", autouse=True)
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="function", loop_scope="session", autouse=True)
async def session():
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope="function", loop_scope="session", autouse=True)
async def existing_table():
    async with async_session_maker() as session:
        test_table = Table(
            name=fake.name(), seats=randint(1, 20), location=fake.word()
        )
        session.add(test_table)
        await session.commit()

        yield test_table


@pytest_asyncio.fixture(scope="function", loop_scope="session", autouse=True)
async def existing_reservation(session, existing_table):
    test_reservation = Reservation(
        customer_name=fake.name(),
        reservation_time=datetime.fromisoformat(fake.iso8601()),
        duration_minutes=60,
        table_id=existing_table.id
    )
    session.add(test_reservation)
    await session.commit()

    yield test_reservation


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def cleanup_created_entities():
    yield

    async with async_session_maker() as session:
        await session.execute(
            Reservation.__table__.delete()
        )
        await session.execute(
            Table.__table__.delete()
        )

        await session.commit()
