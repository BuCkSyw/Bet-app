from fastapi import APIRouter, HTTPException

from app.dao import BetsDao
from app.schemas import ChangeBetStatusRequest, SBEts

router = APIRouter(
    prefix="/bets",
    tags=["Ставки"],
)


@router.put(
    "/callback_change_status", name="Обратный вызов смены статуса событий"
)
async def change_status_bet(request_data: ChangeBetStatusRequest):
    await BetsDao.change_status_bet(
        request_data.event_id, request_data.event_status
    )
    return {"msg": f"Event {request_data.event_id} status has been changed"}


@router.post("/bet", name="Сделать ставку")
async def do_bet(bet: SBEts):
    await BetsDao.do_bet(bet)
    return {
        "msg": f"bet with an amount {bet.amount} on the event {bet.event_id} is made"
    }


@router.get("", name="Показать историю ставок")
async def get_all_bets():
    bets = await BetsDao.get_all_bets()
    if not bets:
        raise HTTPException(status_code=404, detail=f"Bets not found")
    return bets
