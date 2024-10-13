from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from materials.models import Courses, Lesson
from materials.paginators import CustomPaginator
from materials.serializers import CoursesSerializer, LessonSerializer, CoursesDetailSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.shortcuts import render

from users.permissions import IsModer, IsOwner


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
