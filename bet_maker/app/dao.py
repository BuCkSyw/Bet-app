from sqlalchemy import insert, select, update

from app.database import async_session_maker
from app.models import Bets
from app.schemas import SBEts


class BetsDao:
    model = Bets

    @classmethod
    async def change_status_bet(cls, event_id: int, event_status: str):
        async with async_session_maker() as session:
            

            bet_status_mapping = {
                "unfinished": "no_played",
                "team_1_won": "win",
                "team_2_won": "lose",
            }

            # Update the bet_status field based on the event_status
            query = (
                update(cls.model.__table__)
                .where(cls.model.event_id == event_id)
                .values({"bet_status": bet_status_mapping[event_status]})
                .returning(cls.model)
            )

            result = await session.execute(query)
            updated_bets = result.scalars().all()

            await session.commit()

            return updated_bets

    @classmethod
    async def do_bet(cls, bet: SBEts, bet_status: str = "no_played"):
        async with async_session_maker() as session:

            bet_data = {**bet.model_dump(), "bet_status": bet_status}

            query = insert(cls.model).values(bet_data)

            await session.execute(query)

            await session.commit()

    @classmethod
    async def get_all_bets(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()
