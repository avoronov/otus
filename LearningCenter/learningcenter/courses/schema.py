import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Course, Teacher, Student


class CourseType(DjangoObjectType):

    class Meta:
        model = Course


class TeacherType(DjangoObjectType):

    class Meta:
        model = Teacher


class StudentType(DjangoObjectType):

    class Meta:
        model = Student


class Query:
    courses = graphene.List(CourseType, limit=graphene.Int())
    teachers = graphene.List(TeacherType, limit=graphene.Int())
    students = graphene.List(StudentType, limit=graphene.Int())

    def resolve_courses(self, *args, **kwargs):
        courses = Course.objects.all()
        if "limit" in kwargs:
            return courses[:kwargs["limit"]]
        return courses

    def resolve_teachers(self, *args, **kwargs):
        teachers = Teacher.objects.all()
        if "limit" in kwargs:
            return teachers[:kwargs["limit"]]
        return teachers

    def resolve_students(self, *args, **kwargs):
        students = Student.objects.all()
        if "limit" in kwargs:
            return students[:kwargs["limit"]]
        return students
