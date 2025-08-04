from django.contrib import admin

from materials.models import Subscription
from .models import Course


@admin.register(Course)
class CourseUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price"
    )
