from httpx import AsyncClient


async def test_get_all_bets(ac: AsyncClient):
    response = await ac.get("/bets")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()
    assert isinstance(data, list)
