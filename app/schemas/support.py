from datetime import datetime
from pydantic import BaseModel
from app.models.support_ticket import TicketStatus, TicketPriority


class SupportTicketCreate(BaseModel):
    player_name: str
    discord_user_id: str | None = None
    message: str


class SupportTicketResponse(BaseModel):
    id: int
    player_name: str
    discord_user_id: str | None
    message: str
    status: TicketStatus
    priority: TicketPriority
    staff_response: str | None
    ai_suggested_response: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class StaffReply(BaseModel):
    ticket_id: int
    response: str
