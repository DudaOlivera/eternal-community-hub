from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.maintenance import MaintenanceCreate, MaintenanceFinish, MaintenanceResponse
from app.services import maintenance_service

router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])


@router.post("", response_model=MaintenanceResponse, status_code=201)
async def create_maintenance(data: MaintenanceCreate, db: AsyncSession = Depends(get_db)):
    return await maintenance_service.create_maintenance(db, data)


@router.post("/finish", response_model=MaintenanceResponse)
async def finish_maintenance(data: MaintenanceFinish, db: AsyncSession = Depends(get_db)):
    result = await maintenance_service.finish_maintenance(db, data.maintenance_id)
    if not result:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return result


@router.get("/active", response_model=MaintenanceResponse | None)
async def get_active(db: AsyncSession = Depends(get_db)):
    return await maintenance_service.get_active_maintenance(db)
