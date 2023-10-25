from rest_framework import serializers

from study_platform.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов"""

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов"""

    class Meta:
        model = Lesson
        fields = '__all__'
