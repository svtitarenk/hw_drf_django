from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import Serializer, ModelSerializer
from materials.models import Courses, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CoursesSerializer(ModelSerializer):

    class Meta:
        model = Courses
        fields = '__all__'


class CoursesDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source='course', many=True)

    def get_lessons(self, course):
        return LessonSerializer(Lesson.objects.filter(course=course.id), many=True).data
    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Courses
        fields = '__all__'
