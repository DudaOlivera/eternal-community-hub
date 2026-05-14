from datetime import datetime
from pydantic import BaseModel


class EventCreate(BaseModel):
    name: str
    description: str
    author: str
    event_date: datetime
    use_ai: bool = True


class EventResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    ai_description: str | None
    author: str
    event_date: datetime
    active: bool
    sent_discord: bool
    created_at: datetime

    model_config = {"from_attributes": True}
