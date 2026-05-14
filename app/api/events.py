from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.services import event_service

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(data: EventCreate, db: AsyncSession = Depends(get_db)):
    return await event_service.create_event(db, data)


@router.get("", response_model=list[EventResponse])
async def list_events(limit: int = 20, db: AsyncSession = Depends(get_db)):
    return await event_service.list_events(db, limit)


@router.get("/{slug}", response_model=EventResponse)
async def get_event(slug: str, db: AsyncSession = Depends(get_db)):
    event = await event_service.get_event_by_slug(db, slug)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
