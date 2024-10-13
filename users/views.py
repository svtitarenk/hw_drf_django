from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from materials.models import Courses
from users.models import User, Payments, Subscription
from users.permissions import IsOwner
from users.serializers import UserSerializer, PaymentsSerializer, UserShortSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # разрешаем всех пользователей создавать аккаунты, без авторизации

    def perform_create(self, serializer):
        # делаем пользователя автоматически активным, присваиваем is_active=True
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        # Если пользователь не является владельцем профиля, возвращаем UserShortSerializer
        if self.action == 'retrieve' and not self.is_owner(self.get_object()):
            return UserShortSerializer
        return super().get_serializer_class()

    def is_owner(self, obj):
        # Проверяем, является ли текущий пользователь владельцем просматриваемого профиля
        return self.request.user == obj

    def get_permissions(self):
        # разрешаем только зарегистрированным пользователям создавать оплаты
        if self.action == ['retrieve']:
            self.permission_classes = (IsAuthenticated | IsOwner,)
        elif self.action == 'update':
            self.permission_classes = (IsOwner,)
        return super().get_permissions()


class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ('payment_date',)
    filterset_fields = ('course', 'lesson', 'payment_type',)

    serializer_class = PaymentsSerializer


class SubscriptionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Courses.objects.all()  # Определяем набор данных, который будет использоваться
    lookup_field = 'id'  # Поле, по которому будем искать курс

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        # Используем GenericAPIView для получения объекта курса
        course = get_object_or_404(self.get_queryset(), id=course_id)

        # Получаем или создаем подписку
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if not created:
            # Если подписка уже существует, удаляем ее
            subscription.delete()
            message = 'Подписка удалена'
        else:
            # Если подписки нет, создаем новую
            message = 'Подписка добавлена'

        return Response({"message": message})
