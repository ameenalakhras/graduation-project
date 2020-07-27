from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class CustomValidationError(APIException):
    # status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        if status_code is None:
            self.status_code = status.HTTP_400_BAD_REQUEST
        else:
            self.status_code = status_code

        self.detail = {"message": detail}
