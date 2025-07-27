from django.contrib import admin

from .models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
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
