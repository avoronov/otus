from rest_framework import routers

from .views import CourseViewSet, TeacherViewSet, StudentViewSet

router = routers.SimpleRouter()
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"teachers", TeacherViewSet, basename="teachers")
router.register(r"students", StudentViewSet, basename="students")

urlpatterns = router.urls
