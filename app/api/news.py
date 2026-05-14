from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.news import NewsCreate, NewsResponse
from app.services import news_service

router = APIRouter(prefix="/api/news", tags=["news"])


@router.post("", response_model=NewsResponse, status_code=201)
async def create_news(data: NewsCreate, db: AsyncSession = Depends(get_db)):
    return await news_service.create_news(db, data)


@router.get("", response_model=list[NewsResponse])
async def list_news(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await news_service.list_news(db, limit, offset)


@router.get("/{slug}", response_model=NewsResponse)
async def get_news(slug: str, db: AsyncSession = Depends(get_db)):
    news = await news_service.get_news_by_slug(db, slug)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news
