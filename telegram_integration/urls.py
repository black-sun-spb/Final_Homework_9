from django.urls import path
from .views import ConnectTelegramView

urlpatterns = [
    path("connect-telegram/", ConnectTelegramView.as_view(), name="connect-telegram"),
]
