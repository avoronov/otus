from courses.models import Course, Teacher, Student
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'title', 'description', 'is_active'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = 'id', 'first_name', 'last_name'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = 'id', 'first_name', 'last_name'
