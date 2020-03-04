from rest_framework import routers
from course.views import MediaViewSet

router = routers.DefaultRouter()

router.register('media', MediaViewSet)
# router.register('permission', PermissionViewSet)

urlpatterns = router.urls
