# this file differs from utils that it's made to hold viewsets functions that don't need self
# and at the same time if put on utils.py it will be causing cercular calling (like classroom class and
# default_class_background_img function inside it).

from rest_framework import status
from rest_framework.response import Response

from classroom.models import ClassRoom, Task
from composeexample.permissions import OnlyEnrolled, OnlyEnrolledRelated
from rest_framework.exceptions import PermissionDenied

from main.models import Attachment
from django.shortcuts import get_object_or_404
from functools import wraps


def check_classroom_exists(f):
    """
    a decorator to check:
        if the classroom requested (dispatcher in the url) exists or not
    it expects the input data to be:
        args : obj, request        ###(while being in order)
        kwargs: pk              ###(which is the classroom id)
    """
    def wrapper(*args, **kwargs):
        obj, request = args
        # some requests take the classroom_pk and an extra pk for another field
        classroom_pk = kwargs.get("classroom_pk", None)
        if classroom_pk is None:
            classroom_pk = kwargs.get("pk", None)

        classroom_exists = ClassRoom.objects.filter(id=classroom_pk).exists()
        if classroom_exists:
            return f(*args, **kwargs)
        else:
            return Response(
                data={"message": "classroom doesn't exist"},
                status=status.HTTP_404_NOT_FOUND
            )

    return wrapper


def check_user_enrolled(f):
    """
    a decorator to check:
        first: checks if the classroom exists or not. (from check_classroom_exists decorator)
        second: if the requester user is inside of the classroom or not,
    it expects the input data to be:
        args : obj, request        ###(while being in order)
        kwargs: pk              ###(which is the classroom id)
    """
    @check_classroom_exists
    def wrapper(*args, **kwargs):
        obj, request = args
        classroom_pk = kwargs.get("classroom_pk", None)
        if classroom_pk is None:
            classroom_pk = kwargs.get("pk", None)

        classroom = ClassRoom.objects.get(id=classroom_pk)
        # checks if the user is enrolled inside of the classroom
        user_enrolled = OnlyEnrolled().has_object_permission(request, view=classroom, obj=classroom)
        if user_enrolled:
            return f(*args, **kwargs)
        else:
            return Response(
                data={"message": "user isn't enrolled in the classroom"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return wrapper


def check_classroom_owner(f):
    """
    a decorator to check:
        first: checks if the classroom exists or not. (from check_classroom_exists decorator).
        second: checks if the requester is the classroom owner himself.

    it expects the input data to be:
        args : obj, request        ###(while being in order)
        kwargs: pk              ###(which is the classroom id)
    """
    @check_classroom_exists
    def wrapper(*args, **kwargs):
        obj, request = args
        classroom_pk = kwargs.get("classroom_pk", None)
        if classroom_pk is None:
            classroom_pk = kwargs.get("pk", None)

        classroom = ClassRoom.objects.get(id=classroom_pk)
        # checks if the user is enrolled inside of the classroom
        if classroom.user == request.user:
            return f(*args, **kwargs)
        else:
            return Response(
                data={"message": "only the classroom owner can perform this action"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return wrapper


def check_attachment_owner(f):
    def wrapper(*args, **kwargs):
        obj, request = args
        attachment_id = request.data.get("attachment", None)
        attachment = get_object_or_404(Attachment, id=attachment_id)
        # checks if the requester user is the attachment owner
        requester_is_owner = (attachment.user == request.user)
        if requester_is_owner:
            return f(*args, **kwargs)
        else:
            return Response(
                data={"message": "you can submit your attachments only."},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return wrapper


def check_requester_is_student(f):
    def wrapper(*args, **kwargs):
        obj, request = args
        student_is_student = request.user.groups.filter(name="students").exists()
        if student_is_student:
            return f(*args, **kwargs)
        else:
            return Response(
                data={"message": "only students can do this request."},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return wrapper


def check_requester_is_teacher(f):
    def wrapper(*args, **kwargs):
        obj, request = args
        student_is_teacher = request.user.groups.filter(name="teachers").exists()
        if student_is_teacher:
            return f(*args, **kwargs)
        else:
            return Response(
                data={"message": "only teachers can do this request."},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return wrapper


def check_task_solution_info_class_owner(f):
    """
    checks if the requester changing the acceptance of the task solutions is the owner of the task submitted
    """
    def wrapper(*args, **kwargs):
        obj, request = args
        task_owner = obj.task_main_model.task.user
        requester = request.user
        if task_owner == requester:
            return f(*args, **kwargs)
        else:
            return Response(
                data={"info": "you don't have the permission to perform this action."},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return wrapper


def check_enrolled_related(model):
    """
    this request is pretty much OnlyEnrolledRelated but that works with create requests since
    OnlyEnrolledRelated doesn't work on create requests

    it takes model as an argument to get its id from the url.

    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _, request = args
            related_pk = kwargs.get("pk", None)
            obj = get_object_or_404(model, id=related_pk)
            user_enrolled = OnlyEnrolledRelated().has_object_permission(request=request, view=obj, obj=obj)
            if user_enrolled:
                return f(*args, **kwargs)
            else:
                return Response(
                    data={"message": "user isn't enrolled in the classroom"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return wrapper
    return decorator

#
# def check_user_enrolled(request, classroom_pk, *args, **kwargs):
#     """
#     checks if the user(requester) is enrolled inside of the requested classroom (from classroom_pk)
#     using the onlyEnrolled permission class that is made for classRoom
#     """
#     classroom = ClassRoom.objects.get(id=classroom_pk)
#     # checks if the user is enrolled inside of the classroom
#     user_enrolled = OnlyEnrolled().has_object_permission(request, view=classroom, obj=classroom)
#     if not user_enrolled:
#         check_status = False
#         exception_response = Response(
#             data={"message": "user isn't enrolled in the classroom"},
#             status=status.HTTP_401_UNAUTHORIZED
#         )
#     else:
#         check_status = True
#         exception_response = None
#     return check_status, exception_response
#
#
# def check_classroom_exists(classroom_id):
#     classroom_exists = ClassRoom.objects.filter(id=classroom_id).exists()
#     if classroom_exists:
#         check_status = True
#         exception_response = None
#     else:
#         check_status = False
#         exception_response = Response(
#             data={"message": "classroom doesn't exist"},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     return check_status, exception_response
