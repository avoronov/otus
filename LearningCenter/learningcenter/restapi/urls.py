from rest_framework import routers

from .views import CourseViewSet, TeacherViewSet, StudentViewSet

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = router.urls
