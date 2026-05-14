from datetime import datetime, timedelta
import asyncio

from app.tasks.celery_app import celery_app
from app.database import AsyncSessionLocal
from app.services import boss_service
from app.integrations import discord_client
from app.config import settings
from sqlalchemy import select
from app.models.boss_spawn import BossSpawn
from app.models.event import Event


@celery_app.task
def check_boss_spawns():
    asyncio.run(_check_boss_spawns())


async def _check_boss_spawns():
    async with AsyncSessionLocal() as db:
        now = datetime.utcnow()
        window = now + timedelta(minutes=30)

        result = await db.execute(
            select(BossSpawn).where(
                BossSpawn.killed == False,
                BossSpawn.notified == False,
                BossSpawn.spawn_time <= window,
                BossSpawn.spawn_time >= now,
            )
        )
        for boss in result.scalars().all():
            await boss_service.notify_boss_spawn(db, boss.id)


@celery_app.task
def send_event_reminders():
    asyncio.run(_send_event_reminders())


async def _send_event_reminders():
    async with AsyncSessionLocal() as db:
        now = datetime.utcnow()
        one_hour = now + timedelta(hours=1)

        result = await db.execute(
            select(Event).where(
                Event.active == True,
                Event.reminder_sent == False,
                Event.event_date <= one_hour,
                Event.event_date >= now,
            )
        )
        events = result.scalars().all()

        for event in events:
            site_url = f"{settings.SITE_BASE_URL}/events/{event.slug}"
            embed = {
                "title": f"⏰ Lembrete: {event.name}",
                "description": f"O evento começa em menos de 1 hora!\n\n🔗 {site_url}",
                "color": 0xFFA500,
                "fields": [{"name": "📅 Horário", "value": event.event_date.strftime("%d/%m/%Y às %H:%M"), "inline": True}],
            }
            await discord_client.send_message(settings.DISCORD_EVENTS_CHANNEL_ID, embed=embed)
            event.reminder_sent = True

        await db.commit()
