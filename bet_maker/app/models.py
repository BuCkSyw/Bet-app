from typing import Literal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.database import Base

BetStatus = Literal["no_played", "win", "lose"]


class Bets(Base):
    __tablename__ = "bets"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int]
    amount: Mapped[float] = mapped_column(Numeric(precision=20, scale=2))
    bet_status: Mapped[BetStatus]

    @validates("amount")
    def validate_amount(self, value):
        if value <= 0:
            raise ValueError("amount must be a strictly positive number.")
        return value
