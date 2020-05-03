from django.db import models
from django.db.models import ForeignKey


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    registered_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.id} {self.full_name}'


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    teacher = ForeignKey(Teacher, models.PROTECT)

    def __str__(self):
        return f'{self.id} {self.title}'


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    registered_at = models.DateTimeField(auto_now_add=True)

    courses = models.ManyToManyField(Course)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.id} {self.full_name}'


class Schedule(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()

    course = ForeignKey(Course, models.PROTECT)
