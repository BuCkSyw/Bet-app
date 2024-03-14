from datetime import datetime

from pydantic import BaseModel, Field, NaiveDatetime

from app.models import EventsStatus


class EventUpdate(BaseModel):
    bet_coef: float = Field(None)
    bet_deadline: NaiveDatetime = Field(datetime.now())
    status_event: EventsStatus = Field(None)

    class ConfigDict:
        from_attributes = True
