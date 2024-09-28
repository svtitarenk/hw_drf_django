from django.urls import path
from rest_framework.routers import SimpleRouter
from materials.models import Courses, Lesson
from materials.apps import LessonsConfig
from materials.views import (
    CoursesViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView)

app_name = LessonsConfig.name
router = SimpleRouter()

router.register('', CoursesViewSet)

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete')
]

urlpatterns += router.urls
