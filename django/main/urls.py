from rest_framework import routers
from main.views import UserProfileViewSet, AttachmentViewSet

router = routers.DefaultRouter()

router.register('user_profile', UserProfileViewSet)
router.register("attachment", AttachmentViewSet)
# router.register('permission', PermissionViewSet)

urlpatterns = router.urls
