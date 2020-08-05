# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from authentication.models import User
from authentication.serializers import UserSerializer
from classroom.serializers import ClassRoomSerializer, CommentsSerializer, TaskSerializer, \
    PostSerializer, MaterialSerializer, ClassroomMaterialSerializer, EditMaterialSerializer, CommentsUpdateSerializer, \
    PostUpdateSerializer, TaskUpdateSerializer, TaskSolutionInfoSerializer, TaskSolutionInfoUpdateSerializer, \
    EditClassRoomSerializer, PostListSerializer, CleanClassRoomSerializer
from classroom.models import ClassRoom, Comments, Task, Post, Material, TaskSolutionInfo, TaskSolution
from classroom.utils import generate_promo_code
from classroom.views_utils import check_user_enrolled, check_classroom_owner, check_attachment_owner, \
    check_requester_is_teacher, check_requester_is_student, check_task_solution_info_class_owner, \
    check_enrolled_related
from composeexample.permissions import OwnerEditOnly, OnlyTeacherCreates, \
    OnlyEnrolled, OwnerOnlyDeletesAndEdits, OnlyEnrolledRelated, OwnerAndTeacherDeleteOnly
from course.serializers import CourseSerializer, CourseListSerializer


class ClassRoomViewSetRoot(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all().order_by("-created_at")
    serializer_class = CleanClassRoomSerializer
    permission_classes = [IsAuthenticated, OnlyEnrolled, OnlyTeacherCreates]

    def list(self, request, *args, **kwargs):
        teachers_group = Group.objects.get(name="teachers")
        students_group = Group.objects.get(name="students")
        user = self.request.user
        user_group = self.request.user.groups.first()
        if user_group == students_group:
            queryset = user.student_classrooms.filter(archived=False).order_by("-created_at")
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif user_group == teachers_group:
            queryset = user.teacher_classrooms.filter(archived=False).order_by("-created_at")
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


class UncleanClassRoomViewSetRoot(ClassRoomViewSetRoot):
    queryset = ClassRoom.objects.all().order_by("-created_at")
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated, OnlyEnrolled, OnlyTeacherCreates]


class ClassRoomViewSet(ClassRoomViewSetRoot):
    # OnlyEnrolled doesn't work on Post requests ( because its function is has_object_permission)
    # so it won't work on enroll function and it will only work on destroy function
    permission_classes = [IsAuthenticated, OnlyEnrolled, OwnerEditOnly]
    queryset = ClassRoom.objects.all().order_by("-created_at")
    serializer_class = CleanClassRoomSerializer

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

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = EditClassRoomSerializer

        return serializer_class

    @check_classroom_owner
    def unroll(self, request, *args, **kwargs):
        """
        classroom owner unrolls students from classroom.
        """
        obj = self.get_object()
        user_id = request.data.get("student", None)
        student = get_object_or_404(self.get_object().students, id=user_id)
        obj.students.remove(student)
        obj.save()

        return Response(data={
            "message": "the student has been removed from the classroom."
        }, status=status.HTTP_200_OK)

    @check_classroom_owner
    def accept(self, request, *args, **kwargs):
        """accept a student request of joining the classroom."""
        obj = self.get_object()
        user_id = request.data.get("student", None)
        student = get_object_or_404(self.get_object().student_requests, id=user_id)
        obj.student_requests.remove(student)
        obj.students.add(student)
        obj.save()
        return Response(data={
            "message": "The student has been added to the classroom."
        }, status=status.HTTP_200_OK)

    @check_classroom_owner
    def reject(self, request, *args, **kwargs):
        """reject a student request of joining the classroom"""
        obj = self.get_object()
        user_id = request.data.get("student", None)
        student = get_object_or_404(self.get_object().student_requests, id=user_id)
        obj.student_requests.remove(student)
        obj.save()
        return Response(data={
            "message": "The student request has been rejected."
        }, status=status.HTTP_200_OK)

    @check_classroom_owner
    def add_student(self, request, *args, **kwargs):
        """ add a student by a teacher (using student username)"""
        obj = self.get_object()
        student_username = request.data.get("student", None)
        classroom_students = self.get_object().students
        student_enrolled = classroom_students.filter(username=student_username).exists()
        if student_enrolled:
            return Response(data={
                "message": "The student is already in the classroom"
            }, status=status.HTTP_200_OK)
        student_obj = get_object_or_404(User, username=student_username)
        obj.students.add(student_obj)
        obj.save()
        return Response(data={
            "message": "The student has been added to the classroom."
        }, status=status.HTTP_200_OK)

    def list_students(self, request, *args, **kwargs):
        obj = self.get_object()
        queryset = obj.students
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def list_student_requests(self, request, *args, **kwargs):
        obj = self.get_object()
        queryset = obj.student_requests
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def list_courses(self, request, *args, **kwargs):
        obj = self.get_object()
        queryset = obj.classroom_courses
        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)


class UncleanClassRoomViewSet(ClassRoomViewSet):
    permission_classes = [IsAuthenticated, OnlyEnrolled, OwnerEditOnly]
    queryset = ClassRoom.objects.all().order_by("-created_at")
    serializer_class = ClassRoomSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all().order_by("-created_at")
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyDeletesAndEdits]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = CommentsUpdateSerializer

        elif self.request.method == 'GET':
            serializer_class = PostListSerializer

        return serializer_class

    @check_enrolled_related(model=Post)
    def create(self, request, *args, **kwargs):
        # all the mutable code should be replaced with
        # having the post id in the request data itself
        post_pk = kwargs["pk"]
        request.data._mutable = True
        request.data["post"] = post_pk
        request.data._mutable = False
        return super().create(request, *args, **kwargs)

    @check_enrolled_related(model=Post)
    def list(self, request, *args, **kwargs):
        post_pk = kwargs.get("pk", None)
        self.queryset = self.queryset.filter(post=post_pk)
        return super(CommentViewSet, self).list(request, *args, **kwargs)


class TaskViewSetRoot(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, OnlyTeacherCreates]

    @check_classroom_owner
    def create(self, request, *args, **kwargs):
        classroom_pk = kwargs.get("pk", None)
        request.data._mutable = True
        request.data["classroom"] = classroom_pk
        request.data._mutable = False
        return super(TaskViewSetRoot, self).create(request, *args, **kwargs)

    @check_user_enrolled
    def list(self, request, *args, **kwargs):
        classroom_pk = kwargs.get("pk", None)
        self.queryset = self.get_queryset().filter(classroom=classroom_pk).order_by("-created_at")
        return super(TaskViewSetRoot, self).list(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyDeletesAndEdits, OnlyEnrolledRelated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = TaskUpdateSerializer

        return serializer_class

    def delivered_students_ids(self):
        task_obj = self.get_object()

        task_solutions = task_obj.solution.all()
        delivered_solutions_students_ids = task_solutions.values_list('user', flat=True)
        return delivered_solutions_students_ids

    def delivered_students(self, request, *args, **kwargs):
        task_obj = self.get_object()
        classroom_students = task_obj.classroom.students.all()

        delivered_solutions_students_ids = self.delivered_students_ids()
        delivered_solutions_students = classroom_students.filter(id__in=delivered_solutions_students_ids)
        user_serializer = UserSerializer(delivered_solutions_students, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def undelivered_students(self, request, *args, **kwargs):
        task_obj = self.get_object()
        classroom_students = task_obj.classroom.students.all()

        delivered_solutions_students_ids = self.delivered_students_ids()
        delivered_solutions_students = classroom_students.exclude(id__in=delivered_solutions_students_ids)
        user_serializer = UserSerializer(delivered_solutions_students, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class TaskSolutionInfoViewSet(viewsets.ModelViewSet):
    queryset = TaskSolutionInfo.objects.all().order_by("-created_at")
    serializer_class = TaskSolutionInfoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create_task_solution(self, request, task_solution, *args, **kwargs):
        obj_creation_response = super(TaskSolutionInfoViewSet, self).create(request, *args, **kwargs)
        # 201 : object created successfully
        if obj_creation_response.status_code == 201:
            created_object_id = obj_creation_response.data.get("id", None)
            obj = get_object_or_404(TaskSolutionInfo, id=created_object_id)
            task_solution.solutionInfo.add(obj)

        return obj_creation_response

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = TaskSolutionInfoUpdateSerializer

        return serializer_class

    @check_enrolled_related(model=Task)
    @check_requester_is_student
    @check_attachment_owner
    def create(self, request, *args, **kwargs):
        task_pk = kwargs.get("pk", None)
        task = get_object_or_404(Task, pk=task_pk)
        task_solution_exists = TaskSolution.objects.filter(task=task, user=request.user).exists()
        if task_solution_exists:
            # make sure solution isn't accepted >> create solution info
            task_solution = get_object_or_404(TaskSolution, task=task, user=request.user)
            if task_solution.accepted:
                return Response(
                    data={"info": "you have an accepted solution already, you can't submit more solutions."},
                    status=status.HTTP_403_FORBIDDEN
                )
            else:

                return self.perform_create_task_solution(request, task_solution, *args, **kwargs)
        else:
            task_solution = TaskSolution.objects.create(task=task, user=request.user)
            return self.perform_create_task_solution(request, task_solution, *args, **kwargs)

    @check_requester_is_teacher
    @check_task_solution_info_class_owner
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        task_solution_obj = obj.task_main_model.first()
        one_solution_accepted = task_solution_obj.solutionInfo.filter(accepted=True).exists()
        accepted_status = request.data.get("accepted", None)

        if (accepted_status == "1") or (accepted_status == "True"):
            if not one_solution_accepted:
                response = super(TaskSolutionInfoViewSet, self).update(request, *args, **kwargs)
                one_solution_accepted = task_solution_obj.solutionInfo.filter(accepted=True).exists()

                if one_solution_accepted:
                    task_solution_obj.accepted = True
                    task_solution_obj.save()
                return response
            # if a solution is accepted already
            else:
                return Response(
                    data={"info": "the student has an accepted solution already, you can't accept more solutions."},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif (accepted_status == "0") or (accepted_status == "False"):
            if one_solution_accepted:
                response = super(TaskSolutionInfoViewSet, self).update(request, *args, **kwargs)
                one_solution_accepted = task_solution_obj.solutionInfo.filter(accepted=True).exists()

                if not one_solution_accepted:
                    task_solution_obj.accepted = False
                    task_solution_obj.save()

                return response

            else:
                response = super(TaskSolutionInfoViewSet, self).update(request, *args, **kwargs)
                return response

        else:
            return Response(
                data={"info": "acceptance status isn't recognized."},
                status=status.HTTP_403_FORBIDDEN
            )


class PostViewSetRoot(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]

    @check_user_enrolled
    def create(self, request, *args, **kwargs):
        classroom_pk = kwargs.get("pk", None)
        request.data._mutable = True
        request.data["classroom"] = classroom_pk
        request.data._mutable = False
        return super(PostViewSetRoot, self).create(request, *args, **kwargs)

    @check_user_enrolled
    def list(self, request, *args, **kwargs):
        classroom_pk = kwargs.get("pk", None)
        self.queryset = self.queryset.filter(classroom=classroom_pk)
        self.serializer_class = PostListSerializer
        return super(PostViewSetRoot, self).list(request, *args, **kwargs)


class PostViewSet(PostViewSetRoot):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly, OnlyEnrolledRelated, OwnerAndTeacherDeleteOnly]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = PostUpdateSerializer

        return serializer_class


class MaterialViewSetRoot(viewsets.ModelViewSet):
    queryset = Material.objects.all().order_by("-created_at")
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, OnlyTeacherCreates]

    @check_user_enrolled
    def list_classroom_material(self, request,  *args, **kwargs):
        classroom_pk = self.kwargs["pk"]
        self.queryset = self.get_queryset().filter(classroom=classroom_pk).order_by("-created_at")
        return super(MaterialViewSetRoot, self).list(request, *args, **kwargs)

    @check_classroom_owner
    def create_classroom_material(self, request,  *args, **kwargs):
        classroom_pk = kwargs["pk"]
        request.data._mutable = True
        request.data["classroom"] = classroom_pk
        request.data._mutable = False
        self.serializer_class = ClassroomMaterialSerializer
        return super().create(request)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all().order_by("-created_at")
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyDeletesAndEdits]

    # i use check_user_enrolled decorator instead of OnlyEnrolledRelated permission class because
    # the classroom is a ManyToManyField and not a ForeignKey, so the permission can't scan all
    # the fields related to this one especially.
    @check_user_enrolled
    def partial_update(self, request,  *args, **kwargs):
        self.serializer_class = EditMaterialSerializer
        return super(MaterialViewSet, self).partial_update(request, *args, **kwargs)

    @check_user_enrolled
    def retrieve(self, request, *args, **kwargs):
        classroom_pk = self.kwargs["classroom_pk"]
        self.queryset = self.get_queryset().filter(classroom=classroom_pk).order_by("-created_at")
        return super(MaterialViewSet, self).retrieve(request, *args, **kwargs)

