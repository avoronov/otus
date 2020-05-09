from django.urls import path

from .views import CourseViewSet, TeacherViewSet, StudentViewSet


urlpatterns = [
    path('courses/', CourseViewSet.as_view({'get': 'list'})),
    path('courses/add', CourseViewSet.as_view({'post': 'create'})),
    path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve'})),
    path('courses/<int:pk>/update', CourseViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
    path('courses/<int:pk>/delete', CourseViewSet.as_view({'delete': 'destroy'})),

    path('teachers/', TeacherViewSet.as_view({'get': 'list'})),
    path('teachers/add', TeacherViewSet.as_view({'post': 'create'})),
    path('teachers/<int:pk>/', TeacherViewSet.as_view({'get': 'retrieve'})),
    path('teachers/<int:pk>/update', TeacherViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
    path('teachers/<int:pk>/delete', TeacherViewSet.as_view({'delete': 'destroy'})),

    path('students/', StudentViewSet.as_view({'get': 'list'})),
    path('students/add', StudentViewSet.as_view({'post': 'create'})),  # TODO: teacher is added instead of student, why?
    path('students/<int:pk>/', StudentViewSet.as_view({'get': 'retrieve'})),
    path('students/<int:pk>/update', StudentViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
    path('students/<int:pk>/delete', StudentViewSet.as_view({'delete': 'destroy'})),

    # todo:
    # - assign/unassign teacher to/from course
    # - subscribe/unsubscribe student to/from course
    # - work w/ schedule
]
