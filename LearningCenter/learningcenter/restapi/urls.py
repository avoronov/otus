from django.urls import path

from .views import CourseList, CourseDetail, CourseCreate, CourseUpdate, CourseDelete, TeacherList, TeacherCreate, \
    TeacherDetail, TeacherUpdate, TeacherDelete, StudentList, StudentCreate, StudentDetail, StudentUpdate, StudentDelete

urlpatterns = [
    path('courses/', CourseList.as_view()),
    path('courses/add', CourseCreate.as_view()),
    path('courses/<int:pk>/', CourseDetail.as_view()),
    path('courses/<int:pk>/update', CourseUpdate.as_view()),
    path('courses/<int:pk>/delete', CourseDelete.as_view()),

    path('teachers/', TeacherList.as_view()),
    path('teachers/add', TeacherCreate.as_view()),
    path('teachers/<int:pk>/', TeacherDetail.as_view()),
    path('teachers/<int:pk>/update', TeacherUpdate.as_view()),
    path('teachers/<int:pk>/delete', TeacherDelete.as_view()),

    path('students/', StudentList.as_view()),
    path('students/add', StudentCreate.as_view()),  # TODO: teacher is added instead of student, why?
    path('students/<int:pk>/', StudentDetail.as_view()),
    path('students/<int:pk>/update', StudentUpdate.as_view()),
    path('students/<int:pk>/delete', StudentDelete.as_view()),

    # todo:
    # - assign/unassign teacher to/from course
    # - subscribe/unsubscribe student to/from course
    # - work w/ schedule
]
