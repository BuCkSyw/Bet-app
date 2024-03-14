from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker
from app.models import Events, EventsStatus
from app.schemas import EventUpdate


class LineProviderDao:
    model = Events

    @classmethod
    async def get_all_event(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_actual_event(cls, datetime_now: datetime):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).where(
                cls.model.bet_deadline > datetime_now
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_one_event(cls, event_id):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).where(
                Events.id == event_id
            )
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def del_events(cls, event_id):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == event_id)
            del_event = await session.execute(query)
            await session.commit()
            return bool(del_event.rowcount)

    @classmethod
    async def change_event(cls, event_id: int, event_update: EventUpdate):
        async with async_session_maker() as session:

            query_change_event = select(cls.model.__table__.columns).where(
                Events.id == event_id
            )
            change_event = await session.execute(query_change_event)
            change_event = change_event.mappings().one_or_none()

            if not change_event:
                raise HTTPException(
                    status_code=404, detail="Event doesn`t found"
                )

            update_data = event_update.model_dump(exclude_none=True)

            if "bet_coef" in update_data and update_data["bet_coef"] < 0:
                raise HTTPException(
                    status_code=404, detail="bet_coef must be greater than 0"
                )
            elif "bet_deadline" in update_data:
                if (
                    update_data["bet_deadline"] <= datetime.now()
                    and update_data["status_event"] == "unfinished"
                ):
                    raise HTTPException(
                        status_code=404,
                        detail="event is over, status_event can be only team_1_won or team_2_won",
                    )
                elif (
                    update_data["bet_deadline"] > datetime.now()
                    and update_data["status_event"] != "unfinished"
                ):
                    raise HTTPException(
                        status_code=404,
                        detail="event is not over, status_event can be only unfinished",
                    )
            elif (
                change_event["bet_deadline"]
                and change_event["bet_deadline"] <= datetime.now()
            ):
                if (
                    change_event["status_event"] == "unfinished"
                    and "status_event" not in update_data
                ):
                    raise HTTPException(
                        status_code=404,
                        detail="event is over, status_event can be only team_1_won or team_2_won",
                    )
                elif (
                    change_event["bet_deadline"] > datetime.now()
                    and update_data["status_event"] != "unfinished"
                ):
                    raise HTTPException(
                        status_code=404,
                        detail="event is not over, status_event can be only unfinished",
                    )

            stmt = (
                update(cls.model)
                .where(cls.model.id == event_id)
                .values(**update_data)
                .returning(cls.model)
            )

            result = await session.execute(stmt)
            updated_event = result.scalars().first()

            await session.commit()
            return updated_event

    @classmethod
    async def insert_event(
        cls, bet_coef: float, bet_deadline: datetime, status: EventsStatus
    ):
        async with async_session_maker() as session:
            data = {
                "bet_coef": bet_coef,
                "bet_deadline": bet_deadline,
                "status_event": status,
            }
            if data["bet_coef"] and data["bet_coef"] < 0:
                raise HTTPException(
                    status_code=404, detail="bet_coef must be greater than 0"
                )
            elif (
                data["bet_deadline"] <= datetime.now()
                and data["status_event"] == "unfinished"
            ):
                raise HTTPException(
                    status_code=404,
                    detail="event is over, status_event can be only team_1_won or team_2_won",
                )
            elif (
                data["bet_deadline"] >= datetime.now()
                and (data["status_event"] == "team_1_won"
                or data["status_event"] == "team_2_won")
            ):
                raise HTTPException(
                    status_code=404,
                    detail="event is not over, status_event can be only unfinished",
                )
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
