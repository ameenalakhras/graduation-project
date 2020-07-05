# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

from classroom.serializers import ClassRoomSerializer, CommentsSerializer, TaskSerializer, \
    PostSerializer, MaterialSerializer, ClassroomMaterialSerializer, PutMaterialSerializer
from classroom.models import ClassRoom, Comments, Task, Post, Material
from classroom.utils import generate_promo_code
from composeexample.permissions import OwnerEditOnly, OnlyTeacherCreates, \
    OnlyEnrolled, OwnerDeleteOnly


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
    permission_classes = [IsAuthenticated, OnlyEnrolled]

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
    permission_classes = [IsAuthenticated, OwnerEditOnly]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.filter(deleted=False)
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, OnlyTeacherCreates]

    def check_classroom_exists(self, classroom_id):
        classroom_exists = self.get_queryset().filter(classroom=classroom_id).exists()
        if classroom_exists:
            check_status = True
            exception_response = None
        else:
            check_status = False
            exception_response = Response(
                data={"message": "classroom doesn't exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        return check_status, exception_response

    def check_user_enrolled(self, request, classroom_pk, *args, **kwargs):
        """
        checks if the user(requester) is enrolled inside of the requested classroom (from classroom_pk)
        using the onlyEnrolled permission class that is made for classRoom
        """
        classroom = ClassRoom.objects.get(id=classroom_pk)
        # checks if the user is enrolled inside of the classroom
        user_enrolled = OnlyEnrolled().has_object_permission(request, view=self, obj=classroom)
        if not user_enrolled:
            check_status = False
            exception_response = Response(
                data={"message": "user isn't enrolled in the classroom"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            check_status = True
            exception_response = None
        return check_status, exception_response

    def list_classroom_material(self, request,  *args, **kwargs):
        classroom_pk = self.kwargs["classroom_pk"]
        check_status, exception_response = self.check_classroom_exists(classroom_pk)
        if check_status:
            check_status, exception_response = self.check_user_enrolled(request, classroom_pk)
            if check_status:
                self.queryset = self.get_queryset().filter(classroom=classroom_pk)
                return super(MaterialViewSet, self).list(request)
            else:
                return exception_response
        else:
            return exception_response

    def create_classroom_material(self, request,  *args, **kwargs):
        # if the user isn't the teacher of the classroom_pk, he can't create the material
        classroom_pk = self.kwargs["classroom_pk"]

        if self.check_classroom_exists(classroom_pk):

            classroom = ClassRoom.objects.get(id=classroom_pk)
            if classroom.user == request.user:
                request.data._mutable = True
                request.data["classroom"] = classroom_pk
                request.data._mutable = False
                self.serializer_class = ClassroomMaterialSerializer

                return super(MaterialViewSet, self).create(request)
            else:
                return Response(
                    data={"message": "only the classroom teacher can create material inside it"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data={"message": "classroom doesn't exist"},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request,  *args, **kwargs):
        self.serializer_class = PutMaterialSerializer
        return super(MaterialViewSet, self).partial_update(request)

    def retrieve(self, request, *args, **kwargs):
        classroom_pk = self.kwargs["classroom_pk"]
        classroom_exists, exception_response = self.check_classroom_exists(classroom_pk)
        if classroom_exists:
            user_enrolled, exception_response = self.check_user_enrolled(request, classroom_pk)
            if user_enrolled:
                self.queryset = self.get_queryset().filter(classroom=classroom_pk)
                return super(MaterialViewSet, self).retrieve(request)
            else:
                return exception_response
        else:
            return exception_response
