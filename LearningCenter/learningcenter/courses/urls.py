from courses.views import CourseListView, CourseCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView, \
    MessageView
from django.urls import path

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('course/add/', CourseCreateView.as_view(), name='create'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='update'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='delete'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='view'),
    path('message', MessageView.as_view(), name='send_message'),
]
