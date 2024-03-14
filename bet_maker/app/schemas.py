from typing import Literal

from pydantic import BaseModel, validator


class SBEts(BaseModel):

    event_id: int
    amount: float

    class ConfigDict:
        from_attributes = True

    @validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("amount must be a strictly positive number.")
        return value


EventsStatus = Literal["unfinished", "team_1_won", "team_2_won"]


class ChangeBetStatusRequest(BaseModel):
    event_id: int
    event_status: EventsStatus

    class ConfigDict:
        from_attributes = True
