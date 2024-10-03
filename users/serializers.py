from rest_framework.serializers import ModelSerializer

from users.models import User, Payments


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        # fields = '__all__'
        # fields = ('user_id', 'payment_date', 'course_id', 'lesson_id', 'amount', 'payment_type',)
        fields = ('amount',)


class UserSerializer(ModelSerializer):
    payments = PaymentsSerializer(source="user_payment", many=True)

    def get_user_payment(self, user):
        return Payments.objects.filter(user=user)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'payments')
