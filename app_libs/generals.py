"""
    Version: 1.0.0
    Author: MSI Shafik
    descriptions: By this function will get request user IP address
"""

from random import SystemRandom

from django.utils import timezone

from app_libs.loggers import log_info

new_random_obj = SystemRandom()

__all__ = [
    "get_ip", "get_origin", "generate_otp",
]


def get_ip(request):
    """
    By this function we will get requester IP address
    :param request:
    :return:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    log_info().debug("check IP address {}".format(ip))
    return ip


def get_origin(request):
    """
    :param request:
    :return:
    """
    host = request.META.get('HTTP_HOST')
    scheme = request.META.get('wsgi.url_scheme')
    if host and scheme:
        return scheme + "://" + host
    return False


def generate_otp():
    """
    generate 6 digit random otp code
    :return: number
    """
    return {
        "retries": 0,  # "try_limit": 0,
        "created": timezone.now().isoformat(),
        "code": new_random_obj.randrange(100000, 999999),
        "passed": False  # set otp is not passed by default
    }
