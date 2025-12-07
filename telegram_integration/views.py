from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class ConnectTelegramView(APIView):
    """
    API для привязки chat_id Telegram к профилю пользователя.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get("chat_id")
        if not chat_id:
            return Response(
                {"detail": "chat_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile = getattr(request.user, "profile", None)
        if not profile:
            return Response(
                {"detail": "User profile not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile.telegram_chat_id = chat_id
        profile.save()
        logger.info(f"User {request.user.username} connected Telegram chat_id {chat_id}")
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
