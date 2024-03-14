from datetime import datetime

import httpx
from fastapi import APIRouter, HTTPException

from app.dao import LineProviderDao
from app.models import EventsStatus
from app.schemas import EventUpdate

router = APIRouter(
    prefix="/events",
    tags=["События"],
)


@router.get("/all", name="Показать все события")
async def get_all_events():
    events = await LineProviderDao.get_all_event()
    if not events:
        raise HTTPException(status_code=404, detail=f"Events not found")
    return events


@router.get("", name="Показать актуальные события")
async def get_actual_events():
    events = await LineProviderDao.get_actual_event(datetime_now=datetime.now())
    if not events:
        raise HTTPException(status_code=404, detail=f"Events not found")
    return events


@router.get("/{id}", name="Отображение события по id")
async def get_event_by_id(event_id: int):
    event = await LineProviderDao.get_one_event(event_id)
    if not event:
        raise HTTPException(
            status_code=404, detail=f"Event {event_id} not found"
        )
    return event


@router.put("/change_event/{id}", name="Внести изменения в событие")
async def change_event(id: int, event_update: EventUpdate):
    await LineProviderDao.change_event(id, event_update)
    if event_update.status_event:
        async with httpx.AsyncClient(
            base_url="http://bet_maker:8001"
        ) as client:
            callback_url = "/bets/callback_change_status"
            data = {"event_id": id, "event_status": event_update.status_event}
            print(data)
            await client.put(
                callback_url,
                json=data,
                headers={"Content-Type": "application/json"},
            )
        return {"msg": f"Event {id} has been change"}


@router.post("/add_new_event", name="Добавить новое событие")
async def add_event(
    bet_coef: float, bet_deadline: datetime, status: EventsStatus
):
    await LineProviderDao.insert_event(bet_coef, bet_deadline, status)
    return {"msg": f"Event has been added"}


@router.delete("/delete_event/{id}", name="Удалить событие")
async def del_event(event_id: int):
    del_event = await LineProviderDao.del_events(event_id)
    if del_event:
        return {"msg": f"Event with id {event_id} delete"}
    else:
        return{"msg": "Event not found"}
