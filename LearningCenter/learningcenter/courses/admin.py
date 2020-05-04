from django.contrib import admin

from .models import Teacher, Course, Student, Schedule


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'registered_at', 'full_name'
    list_display_links = 'id', 'full_name'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'teacher'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'registered_at', 'full_name'
    list_display_links = 'id', 'full_name'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = 'id', 'datetime', 'duration', 'course'
    list_display_links = 'id', 'course'
