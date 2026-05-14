from datetime import datetime
from pydantic import BaseModel


class NewsCreate(BaseModel):
    title: str
    content: str
    author: str
    use_ai: bool = True


class NewsResponse(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    ai_content: str | None
    author: str
    published: bool
    sent_discord: bool
    created_at: datetime

    model_config = {"from_attributes": True}
