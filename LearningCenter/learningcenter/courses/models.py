from django.db import models


class Person(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=30)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    registered_at = models.DateTimeField(verbose_name='Дата и время регистрации', auto_now_add=True)

    class Meta:
        ordering = ["last_name"]
        abstract = True

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.id} {self.full_name}'


class Teacher(Person):
    pass


class Student(Person):
    pass


class Course(models.Model):
    title = models.CharField(verbose_name='Название курса', max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    teacher = models.ForeignKey(Teacher, models.PROTECT, null=True, blank=True)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f'{self.id} {self.title}'


class Schedule(models.Model):
    datetime = models.DateTimeField(verbose_name='Дата и время занятия', auto_now_add=True)
    duration = models.DurationField(verbose_name='Длительность занятия')

    course = models.ForeignKey(Course, models.PROTECT)
