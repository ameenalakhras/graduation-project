from rest_framework import routers
from classroom.views import ClassRoomViewSet, CommentViewSet, TaskViewSet, PostViewSet, ClassRoomTeacherViewSet

router = routers.DefaultRouter()

router.register('classroom', ClassRoomViewSet)
router.register('comment', CommentViewSet)
router.register('task', TaskViewSet)
router.register('post', PostViewSet)
router.register('classroomteacher', ClassRoomTeacherViewSet)
# router.register('profile', UserProfileViewSet)
# router.register('permission', PermissionViewSet)

urlpatterns = router.urls
