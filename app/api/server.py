from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services import maintenance_service, boss_service

router = APIRouter(prefix="/api/server", tags=["server"])


@router.get("/status")
async def server_status(db: AsyncSession = Depends(get_db)):
    active_maintenance = await maintenance_service.get_active_maintenance(db)
    return {
        "online": active_maintenance is None,
        "maintenance": active_maintenance is not None,
        "maintenance_reason": active_maintenance.reason if active_maintenance else None,
    }


@router.get("/bosses")
async def upcoming_bosses(db: AsyncSession = Depends(get_db)):
    bosses = await boss_service.list_upcoming_bosses(db)
    return [
        {
            "id": b.id,
            "boss_name": b.boss_name,
            "location": b.location,
            "spawn_time": b.spawn_time.isoformat(),
            "window_minutes": b.window_minutes,
        }
        for b in bosses
    ]
