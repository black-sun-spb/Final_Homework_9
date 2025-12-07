from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Менеджер для кастомного пользователя
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True")
        return self.create_user(email, password, **extra_fields)


# Пользователь
class User(AbstractUser):
    """Расширенная модель пользователя без username"""
    username = None
    email = models.EmailField(unique=True)
    telegram_id = models.CharField(max_length=64, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    telegram_chat_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} Profile"
