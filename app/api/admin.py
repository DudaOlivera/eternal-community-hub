from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, text

from app.database import get_db
from app.models.news import News
from app.models.event import Event
from app.models.maintenance import Maintenance
from app.models.support_ticket import SupportTicket
from app.models.boss_spawn import BossSpawn
from app.models.ranking import Ranking
from app.models.message_log import MessageLog

router = APIRouter(prefix="/admin", tags=["admin"])


@router.delete("/news", summary="Apagar todas as notícias")
async def delete_all_news(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(News))
    await db.execute(text("ALTER SEQUENCE news_id_seq RESTART WITH 1"))
    await db.commit()
    return {"message": "Todas as notícias foram apagadas."}


@router.delete("/events", summary="Apagar todos os eventos")
async def delete_all_events(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Event))
    await db.execute(text("ALTER SEQUENCE events_id_seq RESTART WITH 1"))
    await db.commit()
    return {"message": "Todos os eventos foram apagados."}


@router.delete("/maintenance", summary="Apagar todo o histórico de manutenções")
async def delete_all_maintenance(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Maintenance))
    await db.execute(text("ALTER SEQUENCE maintenance_id_seq RESTART WITH 1"))
    await db.commit()
    return {"message": "Histórico de manutenções apagado."}


@router.delete("/support", summary="Apagar todos os tickets de suporte")
async def delete_all_support(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(SupportTicket))
    await db.execute(text("ALTER SEQUENCE support_tickets_id_seq RESTART WITH 1"))
    await db.commit()
    return {"message": "Todos os tickets foram apagados."}


@router.delete("/bosses", summary="Apagar todos os boss spawns")
async def delete_all_bosses(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(BossSpawn))
    await db.execute(text("ALTER SEQUENCE boss_spawns_id_seq RESTART WITH 1"))
    await db.commit()
    return {"message": "Todos os boss spawns foram apagados."}


@router.delete("/rankings", summary="Apagar todo o ranking")
async def delete_all_rankings(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Ranking))
    await db.execute(text("ALTER SEQUENCE rankings_id_seq RESTART WITH 1"))
    await db.commit()
    return {"message": "Ranking apagado."}


@router.delete("/all", summary="⚠️ Apagar TUDO do banco de dados")
async def delete_everything(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(MessageLog))
    await db.execute(delete(SupportTicket))
    await db.execute(delete(BossSpawn))
    await db.execute(delete(Ranking))
    await db.execute(delete(Maintenance))
    await db.execute(delete(Event))
    await db.execute(delete(News))
    await db.execute(text("""
        ALTER SEQUENCE news_id_seq RESTART WITH 1;
        ALTER SEQUENCE events_id_seq RESTART WITH 1;
        ALTER SEQUENCE maintenance_id_seq RESTART WITH 1;
        ALTER SEQUENCE support_tickets_id_seq RESTART WITH 1;
        ALTER SEQUENCE boss_spawns_id_seq RESTART WITH 1;
        ALTER SEQUENCE rankings_id_seq RESTART WITH 1;
        ALTER SEQUENCE message_logs_id_seq RESTART WITH 1;
    """))
    await db.commit()
    return {"message": "⚠️ Banco de dados limpo completamente."}
