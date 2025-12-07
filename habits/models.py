from __future__ import annotations
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .validators import validate_duration_seconds, validate_periodicity


class Habit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="habits",
        on_delete=models.CASCADE,
    )
    place = models.CharField(max_length=255, blank=True)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_rewarding = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="related_to",
    )
    periodicity_days = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=255, blank=True)
    estimated_duration_seconds = models.PositiveIntegerField(default=60)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["time", "created_at"]

    def clean(self) -> None:
        """Валидируем модель привычки."""
        if self.related_habit and self.reward:
            raise ValidationError(
                "Нельзя указывать одновременно related_habit и reward."
            )
        if self.is_rewarding and (self.reward or self.related_habit):
            raise ValidationError(
                "У приятной привычки не может быть reward или related_habit."
            )
        validate_duration_seconds(self.estimated_duration_seconds)
        validate_periodicity(self.periodicity_days)

        if self.periodicity_days < 1 or self.periodicity_days > 7:
            raise ValidationError(
                "Периодичность привычки должна быть от 1 до 7 дней."
            )

        if self.related_habit:
            if not self.related_habit.is_rewarding:
                raise ValidationError(
                    "В связанные привычки можно указывать только приятные привычки."
                )
            if self.related_habit.pk == self.pk:
                raise ValidationError("Привычка не может быть связана сама с собой.")

    def __str__(self):
        return f"{self.action} ({'pleasant' if self.is_rewarding else 'useful'})"
