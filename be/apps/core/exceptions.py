from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException


class AbstractBaseError(APIException):
    code = "GEN-0000"

    def __init__(self, detail=None, code=None, status_code=None):

        if status_code:
            self.status_code = status_code
        if detail:
            self.default_detail = detail
        if code:
            code = self.default_code

        detail = {
            "code": self.code,
            **self.default_detail
        }
        super().__init__(detail=detail, code=code)


class ResourceAlreadyExist(AbstractBaseError):
    code = "GEN-0001"
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Resource Already Exist')


class ResourceNotFoundException(AbstractBaseError):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Resource Not Found')
    code = "GEN-0002"


class IncorrectValidate(AbstractBaseError):
    code = "GEN-0003"
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Incorrect Validate')


class DuplicatedResource(AbstractBaseError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Duplicated Resource')
    code = "GEN-0001"


class UserPermissionDenied(AbstractBaseError):
    code = "USER-0001"
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Permission Denied')


class UserUnAuthorized(AbstractBaseError):
    code = "USER-0002"
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('User Unauthorized')
