from httpx import AsyncClient

from app.dao import BetsDao


async def test_do_bet(ac: AsyncClient):
    test_bet_data = {
        "amount": 50.0,
        "event_id": 1,
    }

    response = await ac.post("/bet", json=test_bet_data)

    assert response.status_code == 200

    created_bet_id = response.json()["bet_id"]
    created_bet = await BetsDao.get_bet_by_id(created_bet_id)

    assert created_bet is not None
    assert created_bet.amount == test_bet_data["amount"]
    assert created_bet.event_id == test_bet_data["event_id"]

    invalid_bet_data = {
        "amount": -10.0,
        "event_id": 1,
    }

    response = await ac.post("/bet", json=invalid_bet_data)

    assert response.status_code == 400

    assert "detail" in response.json()
