from rest_framework import serializers

from study_platform.models import Course, Lesson, Payments, Subscribe
from study_platform.validators import lesson_url_validator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков"""
    url_video = serializers.CharField(validators=[lesson_url_validator], read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    """ Сериализатор для подписки"""

    class Meta:
        model = Subscribe
        fields = ("status", "user", "course_subscribe")


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов"""

    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscribe = SubscribeSerializer(many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    def get_subscribe(self, instance):
        return instance.subscribe.user.email

    class Meta:
        model = Course
        fields = ("name", "description", "lesson_count", "lessons", "owner", "subscribe")


class PaymentsSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели платежа """
    class Meta:
        model = Payments
        fields = '__all__'



