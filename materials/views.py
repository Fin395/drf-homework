from datetime import datetime
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модератор').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    def get_permissions(self):
        self.permission_classes = []
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in self.permission_classes]

    # def get_object(self):
    #     new_instance = get_object_or_404(Course, pk=kwargs['pk'])
    #     new_lessons = new_instance.lessons.all()
    #     new_lessons_count = new_lessons.count()
    #
    #     old_lessons = get_object_or_404(Course.objects.prefetch_related('lessons'), pk=kwargs['pk']).lessons.all()
    #     old_lessons_count = old_lessons.count()
    #
    #     if new_lessons_count != old_lessons_count:
    #         get_object_or_404(Course, pk=kwargs['pk']).updated_at = datetime.now()
    #
    #     new_instance.save()
    #     serializer = self.get_serializer(new_instance)
    #     return Response(data=serializer.data)

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        lesson = serializer.save()
        course = lesson.course
        course.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модератор').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        course = lesson.course
        course.save()

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        course = instance.course
        instance.delete()
        course.save()

class SubscriptionAPIView(APIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})


# class CurrentUserAPIView(APIView):
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context



    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', True)
    #     instance = self.get_object()
    #     instance.updated_at = datetime.now()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(data=serializer.data)


