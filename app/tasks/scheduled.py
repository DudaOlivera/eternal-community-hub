from datetime import datetime, timedelta

from celery import Task
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.tasks.celery_app import celery_app
from app.integrations import discord_client
from app.config import settings
from app.models.boss_spawn import BossSpawn
from app.models.event import Event

import asyncio

# Sync engine for Celery workers (avoids asyncio/fork conflicts)
sync_engine = create_engine(
    settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg2://"),
    pool_pre_ping=True,
)


def _run(coro):
    """Run a coroutine in a fresh event loop (safe for forked workers)."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task
def check_boss_spawns():
    now = datetime.utcnow()
    window = now + timedelta(minutes=30)

    with Session(sync_engine) as db:
        bosses = db.execute(
            select(BossSpawn).where(
                BossSpawn.killed == False,
                BossSpawn.notified == False,
                BossSpawn.spawn_time <= window,
                BossSpawn.spawn_time >= now,
            )
        ).scalars().all()

        for boss in bosses:
            spawn_str = boss.spawn_time.strftime("%d/%m/%Y às %H:%M")
            embed = discord_client.build_boss_embed(boss.boss_name, boss.location, spawn_str)
            _run(discord_client.send_message(
                settings.DISCORD_NEWS_CHANNEL_ID, content="@everyone", embed=embed
            ))
            boss.notified = True

        db.commit()


@celery_app.task
def send_event_reminders():
    now = datetime.utcnow()
    one_hour = now + timedelta(hours=1)

    with Session(sync_engine) as db:
        events = db.execute(
            select(Event).where(
                Event.active == True,
                Event.reminder_sent == False,
                Event.event_date <= one_hour,
                Event.event_date >= now,
            )
        ).scalars().all()

        for event in events:
            site_url = f"{settings.SITE_BASE_URL}/news.html"
            embed = {
                "title": f"⏰ Lembrete: {event.name}",
                "description": f"O evento começa em menos de 1 hora!\n\n🔗 {site_url}",
                "color": 0xFFA500,
                "fields": [{"name": "📅 Horário", "value": event.event_date.strftime("%d/%m/%Y às %H:%M"), "inline": True}],
            }
            _run(discord_client.send_message(settings.DISCORD_EVENTS_CHANNEL_ID, embed=embed))
            event.reminder_sent = True

        db.commit()
