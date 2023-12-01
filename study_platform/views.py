from datetime import datetime, timezone

from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study_platform.models import Course, Lesson, Payments, Subscribe
from study_platform.paginators import ListPaginator
from study_platform.permissions import IsModerator, IsOwner, IsSuperUser
from study_platform.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscribeSerializer
from study_platform.service import send_message, create_payment
from study_platform.tasks import send_update
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
        super().perform_update(serializer)
        data = serializer.data.get('subscribe')
        last_date = datetime.fromisoformat(serializer.data.get('last_update')).replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        difference = now - last_date
        if data and difference.total_seconds() > 4 * 60 * 60:
            for d in data:
                to_email = User.objects.get(pk=d['user'])
                send_update.delay(to_email.email)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
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
            send_message(subject="Удаление курса",
                         message="Курс был удален",
                         recipient_list=[to_email]
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


class PaymentsCreateAPIView(generics.CreateAPIView):
    """ Создание платежа """
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        data_course = Course.objects.get(pk=self.request.data['payed_course'])
        if data_course is not None:
            id_strip = create_payment(data_course.price)
        else:
            data_lesson = Lesson.objects.get(pk=[self.request.data['payed_lesson']])
            id_strip = create_payment(data_lesson.price)

        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.stripe_id = id_strip
        new_payment.save()


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    """ Получение платежа """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


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


class CourseAPIListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
