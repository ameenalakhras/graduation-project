from rest_framework import routers
from course.views import MediaViewSet, CourseViewSet
from django.urls import path, include

app_name = 'course'

router = routers.DefaultRouter()

router.register('media', MediaViewSet, basename="media")
router.register('course', CourseViewSet, basename="course")

urlpatterns = [
    path('', include(router.urls)),
]
