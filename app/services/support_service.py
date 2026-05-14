from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.support_ticket import SupportTicket, TicketPriority, TicketStatus
from app.schemas.support import SupportTicketCreate, StaffReply
from app.integrations import discord_client, ai_client
from app.config import settings


async def create_ticket(db: AsyncSession, data: SupportTicketCreate) -> SupportTicket:
    ai_result = await ai_client.classify_support_message(data.message)

    ticket = SupportTicket(
        player_name=data.player_name,
        discord_user_id=data.discord_user_id,
        message=data.message,
        priority=TicketPriority(ai_result.get("priority", "medium")),
        ai_suggested_response=ai_result.get("suggested_response"),
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    embed = discord_client.build_support_embed(
        ticket_id=ticket.id,
        player_name=data.player_name,
        message=data.message,
        priority=ticket.priority.value,
        suggested=ai_result.get("suggested_response", ""),
    )
    await discord_client.send_message(settings.DISCORD_SUPPORT_CHANNEL_ID, embed=embed)

    return ticket


async def reply_ticket(db: AsyncSession, data: StaffReply) -> SupportTicket | None:
    result = await db.execute(select(SupportTicket).where(SupportTicket.id == data.ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        return None

    ticket.staff_response = data.response
    ticket.status = TicketStatus.closed
    await db.commit()
    return ticket
