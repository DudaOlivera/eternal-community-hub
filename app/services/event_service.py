from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.event import Event
from app.schemas.event import EventCreate
from app.integrations import discord_client, ai_client
from app.utils.slug import slugify
from app.config import settings


async def create_event(db: AsyncSession, data: EventCreate) -> Event:
    ai_description = None
    if data.use_ai:
        raw = f"Evento: {data.name} no dia {data.event_date.strftime('%d/%m/%Y às %H:%M')}. {data.description}"
        ai_description = await ai_client.enhance_announcement(raw, "evento")

    slug = slugify(data.name)
    event = Event(
        name=data.name,
        slug=slug,
        description=data.description,
        ai_description=ai_description,
        author=data.author,
        event_date=data.event_date,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)

    site_url = f"{settings.SITE_BASE_URL}/events/{event.slug}"
    announcement = ai_description or data.description
    event_date_str = data.event_date.strftime("%d/%m/%Y às %H:%M")

    embed = discord_client.build_event_embed(data.name, announcement, event_date_str, data.author, site_url)
    event.sent_discord = await discord_client.send_message(
        settings.DISCORD_EVENTS_CHANNEL_ID, embed=embed
    )
    await db.commit()
    return event


async def list_events(db: AsyncSession, limit: int = 20) -> list[Event]:
    result = await db.execute(
        select(Event).where(Event.active == True).order_by(Event.event_date.asc()).limit(limit)
    )
    return list(result.scalars().all())


async def get_event_by_slug(db: AsyncSession, slug: str) -> Event | None:
    result = await db.execute(select(Event).where(Event.slug == slug))
    return result.scalar_one_or_none()
