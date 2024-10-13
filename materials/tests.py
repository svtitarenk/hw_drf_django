from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from materials.models import Lesson, Courses
from users.models import User


class LessonListTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create(email='test@test')
        self.course = Courses.objects.create(name="Deploy")
        self.lesson = Lesson.objects.create(
            name="Python",
            course=self.course,
            owner=user
        )
        Lesson.objects.create(
            name="Python2",
            course=self.course,
            owner=user
        )

        self.client.force_authenticate(user=user)

    def test_get_list(self):
        url = reverse('materials:lesson')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lesson(self):
        url = reverse('materials:lesson_retrieve', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Python')

    def test_create_lesson(self):
        self.data = {
            "name": "Test validation url",
            "video_link": "https://www.rutube.ru/watch?v=Ix97CZvelmE"
        }
        url = reverse('materials:lesson_create')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson(self):
        url = reverse('materials:lesson_update', kwargs={'pk': self.lesson.pk})
        self.data = {"name": "C++"}
        response = self.client.patch(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        url = reverse("materials:lesson_delete", kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Exception):
            Lesson.objects.get(pk=self.lesson.pk)
