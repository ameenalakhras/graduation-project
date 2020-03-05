from rest_framework import routers
from mail.views import MailViewSet

router = routers.DefaultRouter()

router.register('mail', MailViewSet)
# router.register('permission', PermissionViewSet)

urlpatterns = router.urls
