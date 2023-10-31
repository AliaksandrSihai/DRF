from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study_platform.models import Course, Lesson, Payments
from study_platform.permissions import IsModerator, IsOwner
from study_platform.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ CRUD для модели курса """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise PermissionDenied("Модераторы не могут создавать уроки")
        elif self.request.user.is_authenticated:
            new_course = serializer.save()
            new_course.owner = self.request.user
            new_course.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user.is_staff:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = queryset.filter(owner=self.request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    """ Класс для создания модели урока """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            return PermissionDenied("Модераторы не могут создавать уроки")
        else:
            new_lesson = serializer.save()
            new_lesson.owner = self.request.user
            new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """ Класс для просмотра созданных уроков """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Lesson.objects.all()
        else:
            queryset = Lesson.objects.filter(owner=self.request.user)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Класс для просмотра созданных уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Класс для полного или частичного обновления созданных уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """  Класс для удаления созданных уроков """

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class PaymentsListAPIView(generics.ListAPIView):
    """ Класс для вывода платежей """

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('payments_date', 'payed_lesson', 'payed_course', 'payments_ways')
