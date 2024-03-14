import asyncio
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import bet_settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.models import Bets


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    assert bet_settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("app/tests/mock_bets.json", "r") as file:
        bets = json.load(file)

    async with async_session_maker() as session:
        add_bets = insert(Bets).values(bets)

        await session.execute(add_bets)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
