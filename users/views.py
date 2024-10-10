from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from users.models import User, Payments
from users.permissions import IsOwner
from users.serializers import UserSerializer, PaymentsSerializer, UserShortSerializer


class UserCreateAPIView(CreateAPIView):
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
