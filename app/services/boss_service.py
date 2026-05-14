from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.boss_spawn import BossSpawn
from app.integrations import discord_client
from app.config import settings


async def create_boss_spawn(
    db: AsyncSession,
    boss_name: str,
    location: str,
    spawn_time: datetime,
    window_minutes: int = 30,
) -> BossSpawn:
    boss = BossSpawn(
        boss_name=boss_name,
        location=location,
        spawn_time=spawn_time,
        window_minutes=window_minutes,
    )
    db.add(boss)
    await db.commit()
    await db.refresh(boss)
    return boss


async def notify_boss_spawn(db: AsyncSession, boss_id: int) -> None:
    result = await db.execute(select(BossSpawn).where(BossSpawn.id == boss_id))
    boss = result.scalar_one_or_none()
    if not boss or boss.notified:
        return

    spawn_str = boss.spawn_time.strftime("%d/%m/%Y às %H:%M")
    embed = discord_client.build_boss_embed(boss.boss_name, boss.location, spawn_str)
    await discord_client.send_message(settings.DISCORD_NEWS_CHANNEL_ID, content="@everyone", embed=embed)

    boss.notified = True
    await db.commit()


async def list_upcoming_bosses(db: AsyncSession) -> list[BossSpawn]:
    result = await db.execute(
        select(BossSpawn)
        .where(BossSpawn.killed == False, BossSpawn.spawn_time >= datetime.utcnow())
        .order_by(BossSpawn.spawn_time.asc())
        .limit(10)
    )
    return list(result.scalars().all())
