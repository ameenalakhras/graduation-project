from django.urls import path

from classroom.views import ClassRoomViewSet, CommentViewSet, TaskViewSet, PostViewSet, MaterialViewSet, \
    ClassRoomViewSetRoot, PostViewSetRoot
list_create = {"get": "list", "post": "create"}
all_actions = {"get": "retrieve", "delete": "destroy", "post": "create", "put": "partial_update"}
basic_actions = {"get": "retrieve", "delete": "destroy", "post": "create"}
retrieve_destroy = {"get": "retrieve", "delete": "destroy"}

urlpatterns = [
    path('classrooms/<int:classroom_pk>/materials/<int:pk>/',
         MaterialViewSet.as_view(
             actions={"get": "retrieve", "delete": "destroy", "put": "partial_update"}
            ), name="material"
         ),
    path('classrooms/<int:classroom_pk>/materials/',
         MaterialViewSet.as_view(actions={"post": "create_classroom_material", "get": "list_classroom_material"}),
         name="material"
         ),
    path('classrooms/', ClassRoomViewSetRoot.as_view(actions=list_create), name="classroom_main"),
    path('classrooms/<int:pk>', ClassRoomViewSet.as_view(actions=retrieve_destroy),
         name="classroom_detail"
         ),
    path('classrooms/<slug:promo_code>/enroll',
         ClassRoomViewSet.as_view(actions={"post": "enroll"}), name="classroom_enroll"
         ),

    path('posts/<int:post>/comments/', CommentViewSet.as_view(
        actions={"post": "create"}),
         name="comment"
         ),
    path('comments/<int:pk>/', CommentViewSet.as_view(
        actions={"delete": "destroy", "put": "partial_update"}),
         name="comment"
         ),
    path('tasks/', TaskViewSet.as_view(actions=basic_actions), name="task"),
    path('posts/', PostViewSetRoot.as_view(actions={"post": "create"}), name="post"),
    path('posts/<int:pk>/', PostViewSet.as_view(
        actions={"get": "retrieve", "delete": "destroy", "put": "partial_update"}),
         name="post"
         ),
]
