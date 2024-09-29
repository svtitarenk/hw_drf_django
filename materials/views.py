from rest_framework.viewsets import ModelViewSet
from materials.models import Courses, Lesson
from materials.serializers import CoursesSerializer, LessonSerializer, CoursesDetailSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.shortcuts import render


# Create your views here.
class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()

    # переопределяем и проверяем. Если у нас действие retrieve, то мы выводим DogDetailSerializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoursesDetailSerializer
        return CoursesSerializer


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
