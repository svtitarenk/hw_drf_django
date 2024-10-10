from rest_framework.serializers import ModelSerializer

from users.models import User, Payments


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = ('amount',)


class UserSerializer(ModelSerializer):
    payments = PaymentsSerializer(source="user_payment", many=True, read_only=True)

    def get_user_payment(self, user):
        return Payments.objects.filter(user=user)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'username', 'email', 'payments')


class UserShortSerializer(ModelSerializer):

    """ При этом для просмотра чужого профиля должна быть доступна только общая информация
        , в которую не входят: пароль, фамилия, история платежей
    """
    class Meta:
        model = User
        # исключить поля
        exclude = (
            'password', 'last_name', 'user_permissions', 'last_login', 'phone', 'is_active',
            'is_staff', 'is_superuser', 'groups',
        )
