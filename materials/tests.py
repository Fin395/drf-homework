from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from materials.models import Course, Lesson
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

        # from rest_framework.test import APITestCase
        # from rest_framework import status
        #
        # from vehicle.models import Car
        #
        #
        # class VehicleTestCase(APITestCase):
        #
        #     def setUP(self):
        #         pass
        #
        #     def test_create_car(self):
        #         """Тестирование создания машины"""
        #         data = {
        #             "title": "test",
        #             "description": "test"
        #         }
        #         response = self.client.post('/cars/', data=data)
        #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #         self.assertEqual(response.json(), {'id': 1, 'milage': [], 'title': 'test', 'description': 'test', 'owner': None})
        #         self.assertTrue(Car.objects.all().exists())
        #
        #     def test_list_car(self):
        #         """Тестирования вывода списка машин"""
        #         Car.objects.create(
        #             title="list test",
        #             description="list test"
        #         )
        #         response = self.client.get(
        #             '/cars/'
        #         )
        #         self.assertEqual(
        #             response.status_code, status.HTTP_200_OK
        #         )
        #         self.assertEqual(response.json(), [{'id': 2, 'milage': [], 'title': 'list test', 'description': 'list test', 'owner': None}])
