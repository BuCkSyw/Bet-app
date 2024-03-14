from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from httpx import Response

from app.main import get_events


async def test_get_events():
    mock_response_data = [
        {
            "event_id": 1,
            "bet_coef": 1.6,
            "bet_deadline": "2024-03-15 00:00:00",
            "status_event": "unfinished",
        }
    ]

    # Create a mock AsyncClient
    mock_client = AsyncMock()

    # Set up the expected behavior of the mock client
    mock_response = Response(200, json=mock_response_data)
    mock_client.get.return_value = mock_response

    # Patch the AsyncClient to use the mock_client in your function
    with patch("app.main.httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = mock_response

        # Call the function to test
        result = await get_events()

    # Assertions
    assert result == mock_response_data
    mock_get.assert_called_once_with("/events")


async def test_get_events_not_found():
    mock_response_data = []
    mock_client = AsyncMock()
    mock_response = Response(404, json=mock_response_data)
    mock_client.get.return_value = mock_response

    with patch("app.main.httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = mock_response
        try:
            await get_events()
        except HTTPException as exc:
            assert exc.status_code == 404
            assert exc.detail == "Events not found"

    mock_get.assert_called_once_with("/events")
