from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.

    Поле `owner` автоматически заполняется текущим пользователем.
    Валидация:
    - Нельзя одновременно указывать related_habit и reward.
    - Приятная привычка не может иметь related_habit или reward.
    """

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        related_habit = data.get("related_habit")
        reward = data.get("reward")
        is_rewarding = data.get("is_rewarding")

        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя указывать одновременно related_habit и reward."
            )

        if is_rewarding and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть reward или related_habit."
            )

        return data
