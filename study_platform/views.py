from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from study_platform.models import Course, Lesson, Payments
from study_platform.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ CRUD для модели курса """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """ Класс для создания модели урока """

    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """ Класс для просмотра созданных уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Класс для просмотра созданных уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Класс для полного или частичного обновления созданных уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """  Класс для удаления созданных уроков """

    queryset = Lesson.objects.all()


class PaymentsListAPIView(generics.ListAPIView):
    """ Класс для вывода платежей """

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('payments_date', 'payed_lesson', 'payed_course', 'payments_ways')
