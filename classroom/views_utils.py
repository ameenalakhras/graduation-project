# this file differs from utils that it's made to hold viewsets functions that don't need self
# and at the same time if put on utils.py it will be causing cercular calling (like classroom class and
# default_class_background_img function inside it).

from rest_framework import status
from rest_framework.response import Response

from classroom.models import ClassRoom
from composeexample.permissions import OnlyEnrolled


def check_user_enrolled(request, classroom_pk, *args, **kwargs):
    """
    checks if the user(requester) is enrolled inside of the requested classroom (from classroom_pk)
    using the onlyEnrolled permission class that is made for classRoom
    """
    classroom = ClassRoom.objects.get(id=classroom_pk)
    # checks if the user is enrolled inside of the classroom
    user_enrolled = OnlyEnrolled().has_object_permission(request, view=classroom, obj=classroom)
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


def check_classroom_exists(classroom_id):
    classroom_exists = ClassRoom.objects.filter(id=classroom_id).exists()
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
