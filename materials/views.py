from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from materials.models import Courses, Lesson
from materials.paginators import CustomPaginator
from materials.serializers import CoursesSerializer, LessonSerializer, CoursesDetailSerializer, PaymentSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.shortcuts import render

from users.models import Payment
from users.permissions import IsModer, IsOwner
from users.services import convert_rub_to_usd, create_product_stripe, create_price_stripe, create_stripe_session


# Create your views here.
class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    pagination_class = CustomPaginator

    # переопределяем и проверяем. Если у нас действие retrieve, то мы выводим DogDetailSerializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoursesDetailSerializer
        return CoursesSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer | IsAuthenticated,)  # не модератор
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)  # модератор или владелец
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner | ~IsModer,)  # не модератор и владелец
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPaginator


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer | IsAuthenticated,)

    def perform_create(self, serializer):
        """ Присваиваем владельца уроку """

        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | IsModer,)  # только свои курсы или уроки


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | IsModer,)  # только свои курсы или уроки


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer | IsOwner,)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)  #

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        print('payment.amount:', payment.amount)
        amount_in_usd = convert_rub_to_usd(payment.amount)
        print('amount_in_usd: ', amount_in_usd)
        product = create_product_stripe(payment.course)
        price = create_price_stripe(product, amount_in_usd)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
