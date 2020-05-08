from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses')),
    path('api-token/', include('apitoken.urls')),
    path('api-jwt/', include('jwttoken.urls')),
    path('api-oauth/', include('oauthtoken.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
