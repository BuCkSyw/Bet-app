from httpx import AsyncClient

from app.dao import LineProviderDao


async def test_del_event(ac: AsyncClient):

    event_id_to_delete = 1

    response = await ac.delete(
        f"events/delete_event/{event_id_to_delete}",
        params={"event_id": event_id_to_delete},
    )
    print(response.text)

    assert response.status_code == 200

    assert response.json() == {
        "msg": f"Event with id{event_id_to_delete} delete"
    }

    del_event = await LineProviderDao.get_one_event(event_id_to_delete)

    assert del_event is None
