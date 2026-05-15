from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.ranking import Ranking

router = APIRouter(prefix="/api/ranking", tags=["ranking"])


@router.get("")
async def get_ranking(limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Ranking).order_by(Ranking.pvp_kills.desc()).limit(limit)
    )
    rankings = result.scalars().all()
    return [
        {
            "position": i + 1,
            "player_name": r.player_name,
            "char_class": r.char_class,
            "pvp_kills": r.pvp_kills,
            "pk_count": r.pk_count,
        }
        for i, r in enumerate(rankings)
    ]
