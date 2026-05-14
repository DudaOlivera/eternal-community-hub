from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BossSpawn(Base):
    __tablename__ = "boss_spawns"

    id: Mapped[int] = mapped_column(primary_key=True)
    boss_name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(200))
    spawn_time: Mapped[datetime] = mapped_column(DateTime)
    window_minutes: Mapped[int] = mapped_column(default=30)
    notified: Mapped[bool] = mapped_column(Boolean, default=False)
    killed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
