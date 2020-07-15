# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

from classroom.serializers import ClassRoomSerializer, CommentsSerializer, TaskSerializer, \
    PostSerializer, MaterialSerializer, ClassroomMaterialSerializer, PutMaterialSerializer, CommentsUpdateSerializer, \
    PostUpdateSerializer
from classroom.models import ClassRoom, Comments, Task, Post, Material
from classroom.utils import generate_promo_code
from classroom.views_utils import check_user_enrolled, check_classroom_exists, check_classroom_owner
from composeexample.permissions import OwnerEditOnly, OnlyTeacherCreates, \
    OnlyEnrolled, OwnerOnlyDeletesAndEdits, OnlyEnrolledRelated, OwnerAndTeacherDeleteOnly


class ClassRoomViewSetRoot(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.filter(deleted=False)
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated, OnlyEnrolled, OnlyTeacherCreates]

    def list(self, request, *args, **kwargs):
        teachers_group = Group.objects.get(name="teachers")
        students_group = Group.objects.get(name="students")
        user = self.request.user
        user_group = self.request.user.groups.first()
        if user_group == students_group:
            queryset = user.student_classrooms.filter(archived=False, deleted=False)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif user_group == teachers_group:
            queryset = user.teacher_classrooms.filter(archived=False, deleted=False)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "user isn't registered in any group."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        promo_code = generate_promo_code(length=10)
        user = self.request.user
        request.data._mutable = True
        request.data["promo_code"] = promo_code
        request.data["user"] = user
        request.data._mutable = False
        return super().create(request, *args, **kwargs)


class ClassRoomViewSet(ClassRoomViewSetRoot):
    # OnlyEnrolled doesn't work on Post requests ( because its function is has_object_permission)
    # so it won't work on enroll function and it will only work on destroy function
    permission_classes = [IsAuthenticated, OnlyEnrolled, OwnerEditOnly]

    def destroy(self, request, *args, **kwargs):
        # if the request is coming from the owner of the classroom
        owner_request = (request.user == self.get_object().user)
        if owner_request:
            return super().destroy(request)
        # if the user is one of the students
        # NOTICE: i don't check for the requests where the requester isn't enrolled
        # because it is covered by "onlyEnrolled" permission class
        else:

            self.get_object().students.remove(request.user)
            return Response(
                {"message": "the user was removed from the classroom"}
                ,status=status.HTTP_200_OK
            )

    def enroll(self, request,  *args, **kwargs):
        """
        where the students enroll to the classroom
        """
        queryset = self.get_queryset()
        try:
            promo_code = self.kwargs["promo_code"]
        except KeyError:
            return Response(
                {"message": "promo code not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        else:
            promo_code_exists = queryset.filter(promo_code=promo_code).exists()
            if promo_code_exists:
                obj = queryset.get(promo_code=promo_code)
                user_enrolled = OnlyEnrolled().has_object_permission(request, view=self, obj=obj)
                if user_enrolled:
                    # it will return the class info
                    return HttpResponseRedirect(reverse("classroom_detail", kwargs={"pk": obj.id}))

                else:
                    auto_accept_students = obj.auto_accept_students
                    if auto_accept_students:
                        obj.students.add(request.user)
                        return Response(
                            {"message": "you're now enrolled to the class"},
                            status=status.HTTP_200_OK
                        )
                    else:
                        obj.student_requests.add(request.user)
                        return Response(
                            {"message": "your request has been sent"},
                            status=status.HTTP_200_OK
                        )
            else:
                return Response(
                    {"message": "class not found"},
                    status=status.HTTP_404_NOT_FOUND
                )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.filter(deleted=False)
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyDeletesAndEdits]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = CommentsUpdateSerializer

        return serializer_class

    def create(self, request, *args, **kwargs):
        post_pk = kwargs["pk"]
        post = Post.objects.get(id=post_pk)
        enrolled_in_classroom = OnlyEnrolledRelated().has_object_permission(request, post, post)
        if enrolled_in_classroom:
            request.data._mutable = True
            request.data["post"] = post_pk
            request.data._mutable = False
            return super().create(request, *args, **kwargs)
        else:
            # replace this with a class for this sentence (it exists in django rest somewhere as
            # forbidden permission message
            return Response(
                data={"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly, OwnerOnlyDeletesAndEdits]


class PostViewSetRoot(viewsets.ModelViewSet):
    queryset = Post.objects.filter(deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]

    @check_user_enrolled
    def create(self, request, *args, **kwargs):
        classroom_pk = kwargs.get("pk", None)
        request.data._mutable = True
        request.data["classroom"] = classroom_pk
        request.data._mutable = False
        return super(PostViewSetRoot, self).create(request, *args, **kwargs)


class PostViewSet(PostViewSetRoot):
    queryset = Post.objects.filter(deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly, OnlyEnrolledRelated, OwnerAndTeacherDeleteOnly]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = PostUpdateSerializer

        return serializer_class


class MaterialViewSetRoot(viewsets.ModelViewSet):
    queryset = Material.objects.filter(deleted=False)
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, OnlyTeacherCreates]

    @check_classroom_exists
    @check_user_enrolled
    def list_classroom_material(self, request,  *args, **kwargs):
        classroom_pk = self.kwargs["pk"]
        self.queryset = self.get_queryset().filter(classroom=classroom_pk)
        return super(MaterialViewSetRoot, self).list(request, *args, **kwargs)

    @check_classroom_exists
    @check_classroom_owner
    def create_classroom_material(self, request,  *args, **kwargs):
        classroom_pk = kwargs["pk"]
        request.data._mutable = True
        request.data["classroom"] = classroom_pk
        request.data._mutable = False
        self.serializer_class = ClassroomMaterialSerializer
        return super().create(request)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.filter(deleted=False)
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyDeletesAndEdits]

    # i use check_user_enrolled decorator instead of OnlyEnrolledRelated permission class because
    # the classroom is a ManyToManyField and not a ForeignKey, so the permission can't scan all
    # the fields related to this one especially.
    @check_user_enrolled
    def partial_update(self, request,  *args, **kwargs):
        self.serializer_class = PutMaterialSerializer
        return super(MaterialViewSet, self).partial_update(request, *args, **kwargs)

    @check_user_enrolled
    def retrieve(self, request, *args, **kwargs):
        classroom_pk = self.kwargs["classroom_pk"]
        self.queryset = self.get_queryset().filter(classroom=classroom_pk)
        return super(MaterialViewSet, self).retrieve(request, *args, **kwargs)

