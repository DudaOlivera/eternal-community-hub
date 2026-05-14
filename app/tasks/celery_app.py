from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "lineage2hub",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.scheduled"],
)

celery_app.conf.beat_schedule = {
    # Check for boss spawns every 5 minutes
    "check-boss-spawns": {
        "task": "app.tasks.scheduled.check_boss_spawns",
        "schedule": crontab(minute="*/5"),
    },
    # Send event reminders every 10 minutes
    "send-event-reminders": {
        "task": "app.tasks.scheduled.send_event_reminders",
        "schedule": crontab(minute="*/10"),
    },
}

celery_app.conf.timezone = "America/Sao_Paulo"
