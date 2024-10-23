from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from materials.models import Courses, Lesson
from materials.paginators import CustomPaginator
from materials.serializers import CoursesSerializer, LessonSerializer, CoursesDetailSerializer, PaymentSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from django.shortcuts import render

from materials.tasks import send_message_course_update
from users.models import Payment, Subscription
from users.permissions import IsModer, IsOwner
from users.services import convert_rub_to_usd, create_product_stripe, create_price_stripe, create_stripe_session


class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    pagination_class = CustomPaginator

    # переопределяем и проверяем. Если у нас действие retrieve, то мы выводим CoursesDetailSerializer
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

    def perform_update(self, serializer):
        """ для запуска задачи на  send_message_course_update при изменении курса (update) """

        print('course_update')
        course = serializer.save()
        send_message_course_update.delay(course.pk)
        subscription = Subscription.objects.filter(course=course).first()  # Возможно, subscription не всегда существует

        if serializer.is_valid():
            serializer.save()  # Сохраняем изменения курса

            # Запускаем задачу через Celery, если есть подписка на курс
            if subscription:
                send_message_course_update.delay(subscription.course_id)
                print('subscription is exists: ', subscription)

            return Response(serializer.data, status=status.HTTP_200_OK)

        print("serializer isn't valid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # не работает!
    # использовал совет в комментариях переделать на perform_update
    # @action(detail=True, methods=['PATCH'])
    # def course_update(self, request, pk):
    #     course = get_object_or_404(Courses, pk=pk)
    #     subscription = get_object_or_404(Subscription, pk=course.pk)
    #     serializer = self.get_serializer(course)
    #     if self.action == 'PATCH':
    #         if subscription:
    #             """ then send_mail_about_birthday """
    #             send_message_course_update.delay(subscription.course_id)
    #     return Response(serializer.data)


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
