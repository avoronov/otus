from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses')),
    path('rest-api/', include(('restapi.urls', 'restapi'), namespace='restapi')),
    path('api-jwt/', include(('jwttoken.urls', 'apijwt'), namespace='apijwt')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
