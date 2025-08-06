from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course, Subscription


@shared_task
def send_update_mail(course_id):
    """Отправляет подписчикам сообщение об обновлении курса."""
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course)

    for subscription in subscriptions:
        user_email = subscription.user.email
        send_mail(
        subject=f'Обновление курса "{course}"',
        message=f'Курс "{course}" обновлен!',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email]
    )
