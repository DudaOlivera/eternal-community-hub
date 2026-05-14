from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.support import SupportTicketCreate, SupportTicketResponse, StaffReply
from app.services import support_service

router = APIRouter(prefix="/api/support", tags=["support"])


@router.post("", response_model=SupportTicketResponse, status_code=201)
async def open_ticket(data: SupportTicketCreate, db: AsyncSession = Depends(get_db)):
    return await support_service.create_ticket(db, data)


@router.post("/reply", response_model=SupportTicketResponse)
async def reply_ticket(data: StaffReply, db: AsyncSession = Depends(get_db)):
    result = await support_service.reply_ticket(db, data)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result
