from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.news import News
from app.schemas.news import NewsCreate
from app.integrations import discord_client, ai_client
from app.utils.slug import slugify
from app.config import settings


async def _unique_slug(db: AsyncSession, base: str) -> str:
    """Append a counter to the slug if it already exists."""
    slug = base
    counter = 1
    while True:
        result = await db.execute(select(News).where(News.slug == slug))
        if result.scalar_one_or_none() is None:
            return slug
        slug = f"{base}-{counter}"
        counter += 1


async def create_news(db: AsyncSession, data: NewsCreate) -> News:
    ai_content = None
    if data.use_ai:
        ai_content = await ai_client.enhance_announcement(
            f"{data.title}: {data.content}", "notícia"
        )

    slug = await _unique_slug(db, slugify(data.title))
    news = News(
        title=data.title,
        slug=slug,
        content=data.content,
        ai_content=ai_content,
        author=data.author,
    )
    db.add(news)
    await db.commit()
    await db.refresh(news)

    site_url = f"{settings.SITE_BASE_URL}/news.html"
    announcement = ai_content or data.content

    embed = discord_client.build_news_embed(news.title, announcement, news.author, site_url)
    news.sent_discord = await discord_client.send_message(
        settings.DISCORD_NEWS_CHANNEL_ID, embed=embed
    )
    await db.commit()
    return news


async def list_news(db: AsyncSession, limit: int = 20, offset: int = 0) -> list[News]:
    result = await db.execute(
        select(News)
        .where(News.published == True)
        .order_by(News.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all())


async def get_news_by_slug(db: AsyncSession, slug: str) -> News | None:
    result = await db.execute(select(News).where(News.slug == slug))
    return result.scalar_one_or_none()
