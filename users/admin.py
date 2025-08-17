from django.contrib import admin

from materials.models import Subscription
from .models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "last_login")
    exclude = ["password"]


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "payment_date",
        "paid_lesson",
        "paid_course",
        "amount",
        "paying_method",
    )


@admin.register(Subscription)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user", "course")
