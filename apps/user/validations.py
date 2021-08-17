from django.contrib.auth import authenticate

from app_libs import exceptions
from app_libs.error_codes import ERROR_CODE


def user_data_validation(func):
    """
    user signup and login data validation decorator
    :param func:
    :return:
    :raises:
        - if X is not valid key: KEY_ERROR
        - if X is not valid format: VALUE_ERROR
    """
    keys = ["username", "password"]

    def validation(request, *args, **kwargs):
        if not all(key in request.data.keys() for key in keys):
            raise exceptions.ValidationError(ERROR_CODE.global_codes.KEY_ERROR)
        return func(request, *args, **kwargs)

    return validation


def preference_data_validation(func):
    """
    user perference  validation decorator
    :param func:
    :return:
    :raises:
        - if X is not valid key: KEY_ERROR
        - if X is not valid format: VALUE_ERROR
    """
    keys = ['country', 'source', 'keywords']

    def validation(request, *args, **kwargs):
        if not all(key in keys for key in request.data.keys()):
            raise exceptions.ValidationError(ERROR_CODE.global_codes.KEY_ERROR)
        if not all(isinstance(request.data[key], list) for key in request.data.keys()):
            raise exceptions.ValidationError(ERROR_CODE.global_codes.VALUE_ERROR)
        return func(request, *args, **kwargs)

    return validation
