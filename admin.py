from django.contrib import admin
from .models import Student, Subject, Timetable, Attendance

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Timetable)
admin.site.register(Attendance)
