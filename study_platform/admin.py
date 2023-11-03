from django.contrib import admin

from study_platform.models import Lesson, Course, Subscribe

# Register your models here.
admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(Subscribe)
