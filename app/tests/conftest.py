import asyncio
import json
import pandas as pd
import pytest
from sqlalchemy import insert

from app.config11 import settings
from app.database import Base, async_session_maker, engine


from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.users.models import Users

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mack_json(model: str):
        # with open(f"app/tests/mock_{model}.json", "r") as file:
        #     return json.load(file)

        csv_name = f"app/tests/mock_{model}.csv"
        df = pd.read_csv(csv_name)

        return df





    hotels_df = open_mack_json("hotels")
    rooms_df = open_mack_json("rooms")
    users_df = open_mack_json("users")
    bookings_df = open_mack_json("bookings")



    # async with async_session_maker() as session:
    #     add_hotels = insert(Hotels).values(hotels)
    #     add_users = insert(Users).values(users)
    #     add_bookings = insert(Bookings).values(bookings)
    #
    #     await session.execute(add_hotels)
    #     await session.execute(add_users)
    #     await session.execute(add_bookings)
    #
    #     await session.commit()


# @pytest.fixture(scope="session", autouse=True)
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def autenticate_ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac



@pytest.fixture(scope="function")
async def sessin():
    async with async_session_maker() as session:
        yield session