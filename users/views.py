from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        """
        Создает нового пользователя с хешированным паролем.
        """
        user = User.objects.create_user(**validated_data)
        return user


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    serializer_class = RegisterSerializer
