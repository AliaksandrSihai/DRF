from rest_framework import viewsets, generics
from study_platform.models import Course, Lesson
from study_platform.serializers import CourseSerializer, LessonSerializer


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
