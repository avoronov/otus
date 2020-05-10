import factory

from courses.models import Course, Teacher, Student


class CourseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Course


class TeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Teacher


class StudentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Student
