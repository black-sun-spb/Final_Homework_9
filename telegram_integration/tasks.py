from celery import shared_task
from django.conf import settings
import logging
import requests

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_telegram_message_for_user(self, chat_id: str, text: str):
    """
    Отправка сообщения пользователю в Telegram через Celery-задачу.
    Повторяет попытку при неудаче до 3 раз, с задержкой 10 секунд.
    """
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не найден в настройках.")
        return

    if not chat_id:
        logger.warning("Не передан chat_id для отправки Telegram-сообщения.")
        return

    if not text:
        logger.warning("Попытка отправить пустое сообщение пользователю %s", chat_id)
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

    try:
        with requests.Session() as session:
            response = session.post(url, data=payload, timeout=5)
            response.raise_for_status()
            logger.info("Сообщение успешно отправлено пользователю %s", chat_id)
    except requests.exceptions.RequestException as exc:
        logger.error("Ошибка при отправке сообщения пользователю %s: %s", chat_id, exc)
        try:
            self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            logger.critical("Превышено число попыток отправки Telegram-сообщения пользователю %s", chat_id)
