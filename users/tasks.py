from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_inactive_users():
    """Деактивирует пользователя, проходившего авторизацию более месяца назад."""
    month_ago = timezone.now().today() - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True).filter(last_login__isnull=False).filter(last_login__lt=month_ago)

    for user in inactive_users:
        user.is_active = False
        user.save()
