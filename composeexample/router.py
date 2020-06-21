from rest_framework import routers
from django.urls import path, include

from course.views import MediaViewSet
from classroom.views import ClassRoomViewSet, CommentViewSet, TaskViewSet, PostViewSet#, ClassRoomTeacherViewSet
from mail.views import MailViewSet
from main.views import UserProfileViewSet, AttachmentViewSet

from authentication import urls as authentication_urls


router = routers.DefaultRouter()

# course app
router.register('media', MediaViewSet)
# router.register('permission', PermissionViewSet)

# classroom app
router.register('classroom', ClassRoomViewSet)
router.register('comment', CommentViewSet)
router.register('task', TaskViewSet)
router.register('post', PostViewSet)
# router.register('classroomteacher', ClassRoomTeacherViewSet)

# mail app
router.register('mail', MailViewSet)

# main app
router.register('user_profile', UserProfileViewSet)
router.register("attachment", AttachmentViewSet)
# router.register('permission', PermissionViewSet)


urlpatterns = [
    path('api/',include(router.urls)),
    path("users/", include(authentication_urls, namespace='users'))
]
