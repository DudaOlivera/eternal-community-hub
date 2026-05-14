from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.maintenance import Maintenance
from app.schemas.maintenance import MaintenanceCreate
from app.integrations import discord_client
from app.config import settings


async def create_maintenance(db: AsyncSession, data: MaintenanceCreate) -> Maintenance:
    maintenance = Maintenance(
        reason=data.reason,
        estimated_duration=data.estimated_duration,
        author=data.author,
        started_at=datetime.utcnow(),
    )
    db.add(maintenance)
    await db.commit()
    await db.refresh(maintenance)

    embed = discord_client.build_maintenance_embed(data.reason, data.estimated_duration, data.author)
    maintenance.sent_discord = await discord_client.send_message(
        settings.DISCORD_MAINTENANCE_CHANNEL_ID, content="@everyone", embed=embed
    )
    await db.commit()
    return maintenance


async def finish_maintenance(db: AsyncSession, maintenance_id: int) -> Maintenance | None:
    result = await db.execute(select(Maintenance).where(Maintenance.id == maintenance_id))
    maintenance = result.scalar_one_or_none()
    if not maintenance:
        return None

    maintenance.is_active = False
    maintenance.finished_at = datetime.utcnow()
    await db.commit()

    embed = discord_client.build_maintenance_end_embed()
    await discord_client.send_message(settings.DISCORD_MAINTENANCE_CHANNEL_ID, embed=embed)

    return maintenance


async def get_active_maintenance(db: AsyncSession) -> Maintenance | None:
    result = await db.execute(select(Maintenance).where(Maintenance.is_active == True))
    return result.scalar_one_or_none()
