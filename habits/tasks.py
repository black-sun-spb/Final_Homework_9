from celery import shared_task
from django.utils import timezone
from .models import Habit
from telegram_integration.tasks import send_telegram_message_for_user


@shared_task
def check_and_send_reminders():
    """
    Проверяет привычки, которые нужно выполнить в текущее время,
    и отправляет напоминания через Telegram.
    """
    now = timezone.localtime()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:
        chat_id = getattr(habit.owner.profile, "telegram_chat_id", None)
        if chat_id:
            text = f"Пора выполнить привычку: {habit.action} — {habit.place or ''}".strip()
            send_telegram_message_for_user.delay(chat_id, text)


from celery import shared_task

@shared_task
def test_celery_task():
    print("Celery task works!")
    return "Task completed"
