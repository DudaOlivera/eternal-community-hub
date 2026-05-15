from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    ai_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    author: Mapped[str] = mapped_column(String(100))
    event_date: Mapped[datetime] = mapped_column(DateTime)
    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    sent_discord: Mapped[bool] = mapped_column(Boolean, default=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
