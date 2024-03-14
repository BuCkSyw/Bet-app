from datetime import datetime
from typing import Literal

from sqlalchemy import DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.database import Base

EventsStatus = Literal["unfinished", "team_1_won", "team_2_won"]


class Events(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bet_coef: Mapped[float] = mapped_column(Numeric(precision=4, scale=2))
    bet_deadline: Mapped[datetime] = mapped_column(DateTime)
    status_event: Mapped[EventsStatus]

    @validates("bet_coef")
    def validate_bet_coef(self, value):
        if value <= 0:
            raise ValueError("bet_coef must be a strictly positive number.")
        return value
