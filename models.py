from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    registration_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.registration_number})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    credits = models.IntegerField()

    def __str__(self):
        return self.name


class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject.name} - {self.day}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.date}"
