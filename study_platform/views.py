from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study_platform.models import Course, Lesson, Payments, Subscribe
from study_platform.paginators import ListPaginator
from study_platform.permissions import IsModerator, IsOwner, IsSuperUser
from study_platform.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscribeSerializer
from study_platform.service import send_message
from users.models import User


class CourseViewSet(viewsets.ModelViewSet):
    """ CRUD для модели курса """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = ListPaginator

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise PermissionDenied("Модераторы не могут создавать уроки")
        elif self.request.user.is_authenticated:
            new_course = serializer.save()
            new_course.owner = self.request.user
            new_course.save()

    def perform_update(self, serializer):
        data = serializer.data.get('subscribe')
        for d in data:
            to_email = User.objects.get(pk=d['user'])
            send_message(subject="Обновление курса",
                         message="Курс был обновлен",
                         recipient_list=[to_email.email]
                        )
        return super().update(serializer)

    def list(self, request, *args, **kwargs):
        print("list method called")
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        print("queryset:", queryset)
        if request.user.is_staff:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            queryset = queryset.filter(owner=self.request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def perform_destroy(self, instance):
        course_subscriptions = instance.subscribe.all()
        for d in course_subscriptions:
            to_email = str(d)
            # to_email = User.objects.get(pk=d.user_id)
            send_message(subject="Удаление курса",
                         message="Курс был удален",
                         recipient_list=[to_email] #to_email.email
                         )


class LessonCreateAPIView(generics.CreateAPIView):
    """ Класс для создания модели урока """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise PermissionDenied("Модераторы не могут создавать уроки")
        else:
            new_lesson = serializer.save()
            new_lesson.owner = self.request.user
            new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """ Класс для просмотра созданных уроков """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ListPaginator

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
    permission_classes = [IsAuthenticated, IsModerator | IsOwner | IsSuperUser]


class PaymentsListAPIView(generics.ListAPIView):
    """ Класс для вывода платежей """

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('payments_date', 'payed_lesson', 'payed_course', 'payments_ways')


class SubscribeViewSet(viewsets.ModelViewSet):
    """ CRUD для подписки """
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user.is_staff:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = queryset.filter(user=self.request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
