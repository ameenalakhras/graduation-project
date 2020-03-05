from rest_framework import routers
from course.views import MediaViewSet
from django.urls import path, include


router = routers.DefaultRouter()

router.register('media', MediaViewSet)
# router.register('permission', PermissionViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
