from django.urls import path

from .views import CourseList, CourseDetail, CourseCreate

urlpatterns = [
    path('courses/', CourseList.as_view()),
    path('courses/add', CourseCreate.as_view()),
    path('courses/<int:pk>/', CourseDetail.as_view()),
]
