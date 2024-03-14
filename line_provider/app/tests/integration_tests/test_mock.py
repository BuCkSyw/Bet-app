from unittest.mock import AsyncMock, patch

from httpx import AsyncClient, Response

from app.router import change_event
from app.schemas import EventUpdate


async def test_change_event(ac: AsyncClient):

    bet_maker_url = "/bets/callback_change_status"

    mock_response_data = {"msg": "Event 1 has been change"}

    mock_httpx_client = AsyncMock()

    mock_response = Response(200, json=mock_response_data)
    mock_httpx_client.put.return_value = mock_response

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = mock_httpx_client

        result = await change_event(1, EventUpdate(status_event="team_1_won"))
        print(result)

    print(mock_httpx_client.put.call_args_list)
    mock_httpx_client.put.assert_called_once_with(
        bet_maker_url,
        json={"event_id": 1, "event_status": "team_1_won"},
        headers={"Content-Type": "application/json"},
    )
    assert result == mock_response_data
