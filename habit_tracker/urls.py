from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# === Swagger Schema ===
schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="Документация API для Habit Tracker",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# === URL patterns ===
urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Users app
    path("api/", include("users.urls")),  # <-- регистрация и прочие пользователи

    # Habits app
    path("api/habits/", include("habits.urls")),

    # DRF auth
    path("api-auth/", include("rest_framework.urls")),

    # JWT tokens
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger UI
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    # JSON/YAML schema
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),

    # Telegram integration
    path("api/telegram/", include("telegram_integration.urls")),
]
