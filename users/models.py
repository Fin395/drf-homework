from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите номер телефона"
    )

    phone_number = models.CharField(
        max_length=25,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Укажите номер телефона",
    )

    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    CASH = "Наличные"
    TRANSFER = "Перевод на счет"

    WAY_TO_PAY_CHOICES = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    payment_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата оплаты"
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Отдельно оплаченный урок",
        related_name="payments",
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        related_name="payments",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    paying_method = models.CharField(
        max_length=50,
        choices=WAY_TO_PAY_CHOICES,
        verbose_name="Способ оплаты",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.paid_lesson if self.paid_lesson else self.paid_course} - {self.amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("-payment_date",)
