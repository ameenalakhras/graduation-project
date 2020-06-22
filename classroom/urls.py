# from rest_framework import routers
from django.urls import path

from classroom.views import ClassRoomViewSet, CommentViewSet, TaskViewSet, PostViewSet#, ClassRoomTeacherViewSet

# router = routers.DefaultRouter()

basic_actions = {"get": "retrieve", "delete": "destroy", "post": "create"}

urlpatterns = [
    path('classroom/', ClassRoomViewSet.as_view(actions={"get": "list"}), name="classroom_main"),
    path('classroom/pk/<int:pk>', ClassRoomViewSet.as_view(actions={"get": "retrieve", "delete": "destroy"}), name="classroom_detail"),
    path('classroom/pc/<slug:promo_code>', ClassRoomViewSet.as_view(actions={"post": "enroll"}), name="classroom_enroll"),
    path('comment/', CommentViewSet.as_view(actions=basic_actions), name="comment"),
    path('task/', TaskViewSet.as_view(actions=basic_actions), name="task"),
    path('post', PostViewSet.as_view(actions=basic_actions), name="post"),
]

#
# router.register('classroom', ClassRoomViewSet)
# router.register('comment', CommentViewSet)
# router.register('task', TaskViewSet)
# router.register('post', PostViewSet)
# # router.register('classroomteacher', ClassRoomTeacherViewSet)
# # router.register('profile', UserProfileViewSet)
# # router.register('permission', PermissionViewSet)
#
# urlpatterns = router.urls
