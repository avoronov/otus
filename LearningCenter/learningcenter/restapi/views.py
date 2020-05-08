from courses.models import Course, Teacher, Student
from rest_framework import generics, permissions
from restapi.serializers import CourseSerializer, TeacherSerializer, StudentSerializer


class CourseList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDelete(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TeacherList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDelete(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDelete(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
