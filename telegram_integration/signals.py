# telegram_integration/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def telegram_profile_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Telegram profile for {instance.user.username} created")
