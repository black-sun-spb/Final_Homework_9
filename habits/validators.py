"""
Валидаторы для модели Habit.
"""

from django.core.exceptions import ValidationError


def validate_duration_seconds(value: int) -> None:
    """Проверяет, что время выполнения привычки положительное и не превышает 120 секунд."""
    if value <= 0 or value > 120:
        raise ValidationError(
            "Время выполнения должно быть положительным и не более 120 секунд."
        )


def validate_periodicity(days: int) -> None:
    """Проверяет, что периодичность выполнения привычки от 1 до 7 дней."""
    if days < 1 or days > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")
