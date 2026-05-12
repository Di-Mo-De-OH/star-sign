from rest_framework import status
from rest_framework.exceptions import APIException

class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'not_found.'
    default_detail= "Resource not found."


class ForbiddenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'forbidden.'
    default_detail= "Resource forbidden."

class ExpiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'expired.'
    default_detail= "Resource expired."