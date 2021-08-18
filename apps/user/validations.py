from django.contrib.auth import authenticate

from app_libs import exceptions
from app_libs.error_codes import ERROR_CODE
from app_libs.validators import is_email_valid


def signup_data_validation(func):
    """
    user signup and login data validation decorator
    :param func:
    :return:
    :raises:
        - if X is not valid key: KEY_ERROR
        - if X is not valid format: VALUE_ERROR
    """
    keys = ["username", "password", "email"]

    def validation(request, *args, **kwargs):
        if not all(key in request.data.keys() for key in keys):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.KEY_ERROR,
                                              'hints': 'Required keys: username, password, email'})
        if not is_email_valid(request.data.get('email')):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.VALUE_ERROR, 'hints': 'Invalid email'})
        return func(request, *args, **kwargs)

    return validation


def otp_validation(func):
    """
    OTP data validation decorator
    :param func:
    :return:
    :raises:
        - if X is not valid key: KEY_ERROR
        - if X is not valid format: VALUE_ERROR
    """
    keys = ["username", "otp"]

    def validation(request, *args, **kwargs):
        if not all(key in request.data.keys() for key in keys):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.KEY_ERROR,
                                              'hints': 'Required keys: username, otp'})
        if not all(key in keys for key in request.data.keys()):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.KEY_ERROR,
                                              'hints': 'Allowed keys: username, otp'})
        return func(request, *args, **kwargs)

    return validation


def password_forgot_validation(func):
    """
    Forgot password validation decorator
    :param func:
    :return:
    :raises:
        - if X is not valid key: KEY_ERROR
        - if X is not valid format: VALUE_ERROR
    """
    keys = ["email"]

    def validation(request, *args, **kwargs):
        if not all(key in request.data.keys() for key in keys):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.KEY_ERROR,
                                              'hints': 'Required keys: email'})
        return func(request, *args, **kwargs)

    return validation


def preference_data_validation(func):
    """
    user preference  validation decorator
    :param func:
    :return:
    :raises:
        - if X is not valid key: KEY_ERROR
        - if X is not valid format: VALUE_ERROR
    """
    keys = ['country', 'source', 'keywords']

    def validation(request, *args, **kwargs):
        if not all(key in keys for key in request.data.keys()):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.KEY_ERROR,
                                              'hints': 'Valid keys: country, source ,keywords'})
        if not all(isinstance(request.data[key], list) for key in request.data.keys()):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.VALUE_ERROR,
                                              'hints': 'country, source and keywords receive only array of string'})
        return func(request, *args, **kwargs)

    return validation


def profile_data_validation(func):
    """
    user profile  validation decorator
    :param func:
    :return:
    :raises:
        - if X is not valid key: KEY_ERROR
        - if X is not valid format: VALUE_ERROR
    """
    keys = ['email', 'password', 'name']

    def validation(request, *args, **kwargs):
        if not all(key in keys for key in request.data.keys()):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.KEY_ERROR,
                                              'hints': 'Valid keys: email, password, name'})
        if request.data.get('email') and not is_email_valid(request.data.get['email']):
            raise exceptions.ValidationError({**ERROR_CODE.global_codes.VALUE_ERROR, 'hints': 'Invalid email'})
        return func(request, *args, **kwargs)

    return validation
