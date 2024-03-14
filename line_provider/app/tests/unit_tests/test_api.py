from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient


async def test_get_all_events(ac: AsyncClient):
    response = await ac.get("events/all")

    assert response.status_code == 200


async def test_add_event(ac: AsyncClient):

    data_success = {
        "bet_coef": 1.5,
        "bet_deadline": (datetime.now() + timedelta(days=1)).isoformat(),
        "status": "unfinished",
    }
    response_success = await ac.post(
        "events/add_new_event", params=data_success
    )
    print(response_success.text)
    assert response_success.status_code == 200
    assert response_success.json() == {"msg": "Event has been added"}

    data_invalid_coef = {
        "bet_coef": -1.0,
        "bet_deadline": (datetime.now() + timedelta(days=1)).isoformat(),
        "status": "unfinished",
    }
    response_invalid_coef = await ac.post(
        "events/add_new_event", params=data_invalid_coef
    )
    assert response_invalid_coef.status_code == 404
    assert "bet_coef must be greater than 0" in response_invalid_coef.text

    data_event_over = {
        "bet_coef": 2.0,
        "bet_deadline": (datetime.now() - timedelta(days=1)).isoformat(),
        "status": "unfinished",
    }
    response_event_over = await ac.post(
        "events/add_new_event", params=data_event_over
    )
    assert response_event_over.status_code == 404
    assert (
        "event is over, status_event can be only team_1_won or team_2_won"
        in response_event_over.text
    )


@pytest.mark.parametrize(
    "event_id, event_data, status_code",
    [
        (1, {"status_event": "unfinished"}, 404),
        (
            8,
            {
                "bet_coef": 2.0,
                "bet_deadline": "2024-03-15 00:00:00",
                "status_event": "team_1_won",
            },
            404,
        ),
        (100, {}, 404),
    ],
)
async def test_change_event(ac: AsyncClient, event_id, event_data, status_code):

    response = await ac.put(f"events/change_event/{event_id}", json=event_data)
    print(response.text)

    assert response.status_code == status_code
