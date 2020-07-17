from rest_framework import routers
from main.views import UserProfileViewSet, AttachmentViewSet
from django.urls import path, include


router = routers.DefaultRouter()

router.register('user_profile', UserProfileViewSet)
router.register("attachments", AttachmentViewSet)
# router.register('permission', PermissionViewSet)

# urlpatterns = router.urls
urlpatterns = [
    path('',include(router.urls)),
]
