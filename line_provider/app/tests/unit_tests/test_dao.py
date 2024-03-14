import pytest

from app.dao import LineProviderDao


@pytest.mark.parametrize(
    "event_id, status_event, is_present",
    [
        (1, "team_2_won", True),
        (5, "team_1_won", True),
        (100, "", False),
    ],
)
async def test_get_event_by_id(event_id, status_event, is_present):

    event = await LineProviderDao.get_one_event(event_id)

    if is_present:
        assert event
        assert event.id == event_id
        assert event.status_event == status_event
    else:
        assert not event
