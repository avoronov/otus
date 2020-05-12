import graphene
from graphene_django.types import DjangoObjectType

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
    course = graphene.Field(CourseType, id=graphene.Int())
    teachers = graphene.List(TeacherType, limit=graphene.Int())
    teacher = graphene.Field(TeacherType, id=graphene.Int())
    students = graphene.List(StudentType, limit=graphene.Int())
    student = graphene.Field(StudentType, id=graphene.Int())

    def resolve_courses(self, *args, **kwargs):
        courses = Course.objects.all()
        if "limit" in kwargs:
            return courses[:kwargs["limit"]]
        return courses

    def resolve_course(self, *args, **kwargs):
        if 'id' in kwargs:
            return Course.objects.get(id=kwargs['id'])

    def resolve_teachers(self, *args, **kwargs):
        teachers = Teacher.objects.all()
        if "limit" in kwargs:
            return teachers[:kwargs["limit"]]
        return teachers

    def resolve_teacher(self, *args, **kwargs):
        if 'id' in kwargs:
            return Teacher.objects.get(id=kwargs['id'])

    def resolve_students(self, *args, **kwargs):
        students = Student.objects.all()
        if "limit" in kwargs:
            return students[:kwargs["limit"]]
        return students

    def resolve_student(self, *args, **kwargs):
        if 'id' in kwargs:
            return Student.objects.get(id=kwargs['id'])


class CourseData(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    is_active = graphene.Boolean()


class CourseMutation(graphene.Mutation):
    class Arguments:
        course_id = graphene.Int(required=True)
        course_data = CourseData(required=True)

    result = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    def mutate(root, info, course_id, course_data):
        result = False
        course = None

        try:
            course = Course.objects.get(id=course_id)
        except Course.ObjectDoesNotExist:
            pass

        if course is not None:
            new_title = course_data.get('title')
            if new_title is not None:
                result = True
                course.title = new_title

            new_desc = course_data.get('description')
            if new_desc is not None:
                result = True
                course.description = new_desc

            new_is_active = course_data.get('is_active')
            if new_is_active is not None:
                result = True
                course.is_active = new_is_active

            if result:
                course.save()

        return {
            'result': result,
            'course': course,
        }


class PersonData(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()


class TeacherMutation(graphene.Mutation):
    class Arguments:
        teacher_id = graphene.Int(required=True)
        person_data = PersonData(required=True)

    result = graphene.Boolean()
    teacher = graphene.Field(TeacherType)

    @staticmethod
    def mutate(root, info, teacher_id, person_data):
        result = False
        teacher = None

        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.ObjectDoesNotExist:
            pass

        if teacher is not None:
            new_first_name = person_data.get('first_name')
            if new_first_name is not None:
                result = True
                teacher.first_name = new_first_name

            new_last_name = person_data.get('last_name')
            if new_last_name is not None:
                result = True
                teacher.last_name = new_last_name

            if result:
                teacher.save()

        return {
            'result': result,
            'teacher': teacher,
        }


class StudentMutation(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int(required=True)
        person_data = PersonData(required=True)

    result = graphene.Boolean()
    student = graphene.Field(StudentType)

    @staticmethod
    def mutate(root, info, student_id, person_data):
        result = False
        student = None

        try:
            student = Student.objects.get(id=student_id)
        except Student.ObjectDoesNotExist:
            pass

        if student is not None:
            new_first_name = person_data.get('first_name')
            if new_first_name is not None:
                result = True
                student.first_name = new_first_name

            new_last_name = person_data.get('last_name')
            if new_last_name is not None:
                result = True
                student.last_name = new_last_name

            if result:
                student.save()

        return {
            'result': result,
            'student': student,
        }


class Mutation:
    update_course = CourseMutation.Field()
    update_teacher = TeacherMutation.Field()
    update_student = StudentMutation.Field()
