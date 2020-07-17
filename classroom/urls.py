from django.urls import path

from classroom.views import ClassRoomViewSet, CommentViewSet, TaskViewSet, PostViewSet, MaterialViewSet, \
    ClassRoomViewSetRoot, PostViewSetRoot, MaterialViewSetRoot, TaskViewSetRoot, TaskSolutionInfoViewSet

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
    path('classrooms/<int:pk>/materials/',
         MaterialViewSetRoot.as_view(actions={"post": "create_classroom_material", "get": "list_classroom_material"}),
         name="material"
         ),
    path('classrooms/', ClassRoomViewSetRoot.as_view(actions=list_create), name="classroom_main"),
    path('classrooms/<int:pk>', ClassRoomViewSet.as_view(actions=retrieve_destroy),
         name="classroom_detail"
         ),
    path('classrooms/<slug:promo_code>/enroll',
         ClassRoomViewSet.as_view(actions={"post": "enroll"}), name="classroom_enroll"
         ),

    path('posts/<int:pk>/comments/', CommentViewSet.as_view(
        actions={"post": "create"}),
         name="comment"
         ),
    path('comments/<int:pk>/', CommentViewSet.as_view(
        actions={"delete": "destroy", "put": "partial_update"}),
         name="comment"
         ),
    path('classrooms/<int:pk>/tasks/', TaskViewSetRoot.as_view(
        actions={"post": "create", "get": "list"}
    ), name="task"),
    path('tasks/<int:pk>/', TaskViewSet.as_view(
        actions={"get": "retrieve", "delete": "destroy", "put": "partial_update"}
    ), name="task"),

    path('classrooms/<int:pk>/posts/', PostViewSetRoot.as_view(actions={"post": "create"}), name="post"),
    path('posts/<int:pk>/', PostViewSet.as_view(
        actions={"get": "retrieve", "delete": "destroy", "put": "partial_update"}),
         name="post"
         ),
    path('tasks/<int:pk>/solution/', TaskSolutionInfoViewSet.as_view(
        actions={"post": "create"}
    ), name="task"),
    path('tasks_solution/<int:pk>/', TaskSolutionInfoViewSet.as_view(
        actions={"put": "update"}
    ), name="task_solution_update"),
]
