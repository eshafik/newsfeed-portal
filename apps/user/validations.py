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
