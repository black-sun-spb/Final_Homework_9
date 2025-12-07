"""
URLs для приложения habits.
Реализованы эндпоинты для CRUD операций и получения списка публичных привычек.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, PublicHabitsListView

# Роутер для CRUD привычек пользователя
router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    # Список публичных привычек (доступен всем пользователям)
    path("habits/public/", PublicHabitsListView.as_view(), name="public-habits"),

    # CRUD для привычек текущего пользователя
    path("", include(router.urls)),
]
