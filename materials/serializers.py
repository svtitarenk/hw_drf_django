from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from materials.models import Courses, Lesson
from materials.validators import UrlValidator
from users.models import Subscription, Payment


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(
        validators=[
            UrlValidator(field='video_link')
        ]
    )

    class Meta:
        model = Lesson
        fields = '__all__'


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class CoursesDetailSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source='course', many=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons(self, course):
        return LessonSerializer(Lesson.objects.filter(course=course.id), many=True).data

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course.id).count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Courses
        fields = ['id', 'name', 'description', 'owner', 'lessons', 'lessons_count', 'is_subscribed']


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
