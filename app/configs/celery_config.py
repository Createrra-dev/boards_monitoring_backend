from celery import Celery
from celery.schedules import crontab

from app.configs.base_config import app_settings


celery_app = Celery("tasks", broker=app_settings.REDIS_URL, include=["app.tasks.boards"])


celery_app.conf.beat_schedule = {
    "check_boards_status_every_minute": {
        "task": "check_boards_status",
        "schedule": crontab(),
    }
}