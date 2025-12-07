# telegram_integration/apps.py
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class TelegramIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_integration'

    def ready(self):
        # Подключаем сигналы
        import telegram_integration.signals  # noqa: F401
