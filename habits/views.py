from rest_framework import viewsets, permissions, generics
from rest_framework.pagination import PageNumberPagination

from .models import Habit
from .serializers import HabitSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Пагинация для списка привычек.
    По умолчанию выводит 5 привычек на страницу.
    """
    page_size = 5


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с привычками.
    Каждый пользователь может видеть и редактировать только свои привычки.
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Если действие list — возвращаем привычки текущего пользователя,
        иначе (retrieve, update, destroy) возвращаем все привычки.
        """
        if self.action == "list":
            return Habit.objects.filter(owner=self.request.user)
        return Habit.objects.all()

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя как владельца привычки."""
        serializer.save(owner=self.request.user)


class PublicHabitsListView(generics.ListAPIView):
    """
    Возвращает список публичных привычек (is_public=True).
    Доступно без авторизации.
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]
