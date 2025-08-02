from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.lesson = Lesson.objects.create(title='test lesson', owner=self.user)
        self.course = Course.objects.create(title='test course')
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson-get', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse('materials:lesson-create')
        data = {
            "title": "new lesson",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )
        self.assertEqual(
            data.get('title'), Lesson.objects.get(pk=2).title
        )

    def test_lesson_update(self):
        url = reverse('materials:lesson-update', args=(self.lesson.pk,))
        data = {
            "title": "new test lesson",
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )
        self.assertEqual(
            data.get('title'), "new test lesson"
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": None,
                    "preview": None,
                    "video_reference": None,
                    "course": None,
                    "owner": self.user.pk
                },
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(pk=8, title='test course', owner=self.user)
        # self.subs = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subs_create(self):
        url = reverse('materials:subs-create')
        data = {
            "user": self.user,
            "course": 8
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get("message"), 'подписка добавлена'
        )
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get("message"), 'подписка удалена'
        )

    def test_user_is_subscribed(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get("is_subscribed"), 'подписка оформлена'
        )
