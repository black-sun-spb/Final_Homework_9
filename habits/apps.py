from django.apps import AppConfig


class HabitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habits'

    def ready(self):
        # Подключаем сигналы, если signals.py существует
        try:
            import habits.signals  # noqa: F401
        except ModuleNotFoundError:
            pass
