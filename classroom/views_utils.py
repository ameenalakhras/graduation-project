# this file differs from utils that it's made to hold viewsets functions that don't need self
# and at the same time if put on utils.py it will be causing cercular calling (like classroom class and
# default_class_background_img function inside it).

from rest_framework import status
from rest_framework.response import Response

from classroom.models import ClassRoom
from composeexample.permissions import OnlyEnrolled


def check_classroom_exists(f):
    """
    a decorator to check if the classroom requested exists or not
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
    a decorator to check if the requester user is inside of the classroom or not
    it expects the input data to be:
    args : obj, request        ###(while being in order)
    kwargs: pk              ###(which is the classroom id)
    """
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
