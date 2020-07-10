from django.urls import path

from classroom.views import ClassRoomViewSet, CommentViewSet, TaskViewSet, PostViewSet, MaterialViewSet, \
    ClassRoomViewSetRoot, PostViewSetRoot
list_create = {"get": "list", "post": "create"}
all_actions = {"get": "retrieve", "delete": "destroy", "post": "create", "put": "partial_update"}
basic_actions = {"get": "retrieve", "delete": "destroy", "post": "create"}
retrieve_destroy = {"get": "retrieve", "delete": "destroy"}

urlpatterns = [
    path('classroom/<int:classroom_pk>/material/<int:pk>/',
         MaterialViewSet.as_view(
             actions={"get": "retrieve", "delete": "destroy", "put": "partial_update"}
            ), name="material"
         ),
    path('classroom/<int:classroom_pk>/material/',
         MaterialViewSet.as_view(actions={"post": "create_classroom_material", "get": "list_classroom_material"}),
         name="material"
         ),
    path('classroom/', ClassRoomViewSetRoot.as_view(actions=list_create), name="classroom_main"),
    path('classroom/<int:pk>', ClassRoomViewSet.as_view(actions=retrieve_destroy),
         name="classroom_detail"
         ),
    path('classroom/<slug:promo_code>/enroll',
         ClassRoomViewSet.as_view(actions={"post": "enroll"}), name="classroom_enroll"
         ),

    path('comment/', CommentViewSet.as_view(actions=basic_actions), name="comment"),
    path('task/', TaskViewSet.as_view(actions=basic_actions), name="task"),
    path('post/', PostViewSetRoot.as_view(actions={"post": "create"}), name="post"),
    path('post/<int:pk>/', PostViewSet.as_view(
        actions={"get": "retrieve", "delete": "destroy", "put": "partial_update"}),
         name="post"
         ),
]
