from rest_framework import routers
from mail.views import MailViewSet

router = routers.DefaultRouter()

router.register('mails', MailViewSet)

urlpatterns = router.urls
