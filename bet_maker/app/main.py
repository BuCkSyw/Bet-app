import httpx
from fastapi import FastAPI, HTTPException

from app.router import router as bet_router

app = FastAPI()

app.include_router(bet_router)


@app.get("/events", name="Вывести список событий", tags=["События"])
async def get_events():
    async with httpx.AsyncClient(base_url="http://line_provider:8000") as client:
        response = await client.get("/events")
        events = response.json()
    if not events:
        raise HTTPException(status_code=404, detail="Bets not found")
    return events
