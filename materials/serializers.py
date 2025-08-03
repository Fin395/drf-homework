from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import VideoReferenceValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoReferenceValidator(field="video_reference")]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons_data = LessonSerializer(source="lessons", many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        course_subs = obj.subscriptions
        current_user = self.context["request"].user

        if course_subs.filter(user=current_user).exists():
            return "подписка оформлена"
        else:
            return "подписка не оформлена"

    class Meta:
        model = Course
        fields = "__all__"
