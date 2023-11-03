from study_platform.apps import StudyPlatformConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from study_platform import views

router = DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='course')
router.register(r'subscribe', views.SubscribeViewSet, basename='subscribe')
app_name = StudyPlatformConfig.name

urlpatterns = [
    path('lesson/create/', views.LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', views.LessonListAPIView.as_view(), name='lesson_all'),
    path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson_one'),
    path('lesson/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('payments/', views.PaymentsListAPIView.as_view(), name='payments'),
] + router.urls
