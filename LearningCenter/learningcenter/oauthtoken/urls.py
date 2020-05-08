from django.urls import path, include

from .views import UserList, UserDetail, GroupList

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('groups/', GroupList.as_view()),
]
