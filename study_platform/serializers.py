from rest_framework import serializers
from study_platform.models import Course, Lesson, Payments, Subscribe
from study_platform.service import get_payment
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

    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    subscribe = SubscribeSerializer(many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели платежа """

    course_amount = serializers.SerializerMethodField(read_only=True)
    lesson_amount = serializers.SerializerMethodField(read_only=True)
    stripe_data = serializers.SerializerMethodField(read_only=True)

    def get_stripe_data(self, instance):
        return get_payment(instance.stripe_id)

    def get_course_amount(self, instance):
        payed_course = instance.payed_course
        if payed_course:
            return payed_course.price

    def get_lesson_amount(self, instance):
        payed_lesson = instance.payed_lesson
        if payed_lesson is not None:
            return payed_lesson.price

    class Meta:
        model = Payments
        fields = '__all__'
