"""Celery configuration for the habit_tracker project."""
import os
from celery import Celery

# Устанавливаем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

# Инициализация Celery
app = Celery("habit_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
