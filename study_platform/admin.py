from django.contrib import admin

from study_platform.models import Lesson, Course, Subscribe, Payments

# Register your models here.
admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(Subscribe)
admin.site.register(Payments)
