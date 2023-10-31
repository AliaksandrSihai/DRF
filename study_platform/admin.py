from django.contrib import admin

from study_platform.models import Lesson, Course

# Register your models here.
admin.site.register(Lesson)
admin.site.register(Course)