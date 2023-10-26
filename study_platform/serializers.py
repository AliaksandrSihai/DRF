from rest_framework import serializers

from study_platform.models import Course, Lesson, Payments


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков"""

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов"""

    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ("name", "description", "lesson_count", "lessons")


class PaymentsSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели платежа """
    class Meta:
        model = Payments
        fields = '__all__'
