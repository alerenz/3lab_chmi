from django.contrib import admin

from .models import Authors, Courses, UsersCourses

# Register your models here.
admin.site.register(Authors)
admin.site.register(Courses)
admin.site.register(UsersCourses)
