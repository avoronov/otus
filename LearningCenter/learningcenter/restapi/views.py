from courses.models import Course, Teacher, Student
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from restapi.serializers import CourseSerializer, TeacherSerializer, StudentSerializer


class CourseViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TeacherViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
