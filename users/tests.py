from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from materials.models import Lesson
from .models import Courses, Subscription
from users.models import User


class SubscribeDeleteTestCase(APITestCase):

    # username = 'testuser' email = 'test3@test.ru'
    def setUp(self):
        # Создаем пользователя и курс
        self.user = User.objects.create(email='test3@test.ru')
        self.course = Courses.objects.create(name="Test Course")
        # URL для работы с подписками
        self.subscription_url = reverse('users:subscription-api')  # , args=(self.subscription.pk,))
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Отправляем POST-запрос для создания подписки
        response = self.client.post(self.subscription_url, {'course_id': self.course.id})
        # Проверяем, что подписка успешно создана
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        # Проверяем, что подписка была добавлена в базу данных
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_delete_subscription(self):
        # Создаем подписку вручную для теста удаления
        Subscription.objects.create(user=self.user, course=self.course)

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Отправляем POST-запрос для удаления подписки
        response = self.client.post(self.subscription_url, {'course_id': self.course.id})

        # Проверяем, что подписка успешно удалена
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')

        # Проверяем, что подписка была удалена из базы данных
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_without_authentication(self):
        # Выйдем из системы
        self.client.logout()
        # Отправляем POST-запрос без аутентификации
        response = self.client.post(self.subscription_url, {'course_id': self.course.id})

        # Проверяем, что запрос неавторизован
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
