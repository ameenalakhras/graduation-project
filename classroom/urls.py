from django.urls import path

from classroom.views import ClassRoomViewSet, CommentViewSet, TaskViewSet, PostViewSet, MaterialViewSet#, ClassRoomTeacherViewSet

basic_actions = {"get": "retrieve", "delete": "destroy", "post": "create"}
retrieve_destroy = {"get": "retrieve", "delete": "destroy"}

urlpatterns = [
    path('classroom/', ClassRoomViewSet.as_view(actions={"get": "list", "post":"create"}), name="classroom_main"),
    path('classroom/pk/<int:pk>', ClassRoomViewSet.as_view(actions=retrieve_destroy), name="classroom_detail"),
    path('classroom/pc/<slug:promo_code>', ClassRoomViewSet.as_view(actions={"post": "enroll"}), name="classroom_enroll"),
    path('comment/', CommentViewSet.as_view(actions=basic_actions), name="comment"),
    path('task/', TaskViewSet.as_view(actions=basic_actions), name="task"),
    path('post', PostViewSet.as_view(actions=basic_actions), name="post"),
    path('material/', MaterialViewSet.as_view(actions={"post": "create"}), name="material"),
    path('material/<pk>/', MaterialViewSet.as_view(actions=retrieve_destroy), name="material"),
]