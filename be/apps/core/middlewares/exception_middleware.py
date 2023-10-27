import logging

from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler as drf_exception_handler

from apps.core.exceptions import AbstractBaseError

logger = logging.getLogger()


def set_rollback():
    atomic_requests = connection.settings_dict.get('ATOMIC_REQUESTS', False)
    if atomic_requests and connection.in_atomic_block:
        transaction.set_rollback(True)


def api_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        data = {'message': exc.default_detail}

        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data['errors'] = exc.detail if isinstance(exc.detail, (list, dict)) else (exc.detail,)

        set_rollback()
        logger.info(exc.default_detail)

        return drf_exception_handler(AbstractBaseError(detail=data, status_code=exc.status_code), context)

    return None
