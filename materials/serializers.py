from rest_framework.serializers import Serializer, ModelSerializer
from materials.models import Courses, Lesson


class CoursesSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
