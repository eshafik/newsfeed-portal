"""
    Version: 1.0.0
    Author: MSI Shafik
"""
import datetime

import phonenumbers
from phonenumbers import timezone

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

__author__ = "MSI Shafik"
__version__ = "1.0.0"

import re

__all__ = [
    "is_email_valid", "is_phone_valid",
    "name_validation", "is_amount_valid",
    "is_valid_url", "date_validation",
    "is_sol_email_valid",
]


def is_phone_valid(phone_number: str) -> bool:
    """
    :param phone_number:
    :return: True, correct phone number or False, blank
    :rtype: tuple
    """
    try:
        area_zone = timezone.time_zones_for_number(phonenumbers.parse(phone_number, 'GB'))[0]
    except:
        return False
    if area_zone == "Etc/Unknown":
        return False

    return True


def is_email_valid(email: str) -> bool:
    """
    Check email is valid of not
    :return: True or False
    :rtype: bool
    """
    if email:
        email_regex = re.compile(r'^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.]+$')
        if not email_regex.match(email):
            return False
        else:
            return True
    else:
        return False


def is_amount_valid(amount: str) -> bool:
    """
    :param amount:
    :return: True or False
    :rtype: bool
    """
    new_amount = str(amount)
    amount_regex = re.compile(r'^\d*[.,]?\d*$')
    if amount_regex.match(new_amount):
        return True
    else:
        return False


def is_valid_url(url: str) -> bool:
    """
    Validating A URL
    :param url:
    :return: True or False
    :rtype: bool
    """
    valid_instance = URLValidator()
    try:
        valid_instance(url)
        return True
    except ValidationError as err:
        print(err)
        return False


def name_validation(name: str, *args) -> bool:
    """
    Description: Use proper name.The character should use alphanumerics. You can't use any special characters. Such as
    './%^' etc

    Example:
    In [19]: from app_libs.validators import name_validation
    In [20]: name_validation(name='vubon')
    Out[20]: True

    or You can use
    Example:
    In [21]: name_validation(name='vubon roy')
    Out[21]: True

    You can pass tuple data for validation
    Example:
    In [2]: name_validation(*("vubon roy", "Jamuna bank"))
    Out[2]: True

    But You can't use any special characters
    Example:
    In [13]: name_validation(' $vubon roy ')
    Out[13]: False

    :param name:
    :return:  True or False
    :rtype
    """
    try:
        if args:
            for name in args:
                all_characters = "".join(name.split())
                if all_characters.isalnum():
                    return True
                return False
        if name:
            all_characters = "".join(name.split())
            if all_characters.isalnum():
                return True
            return False

        return False
    except ValueError:
        return False


def date_validation(date: str, *args) -> bool:
    """

    In [13]: from app_libs.validators import date_validation

    In [14]: date_validation(*("2019-1-20", "2019-1-29"))
    Out[14]: True

    In [15]: date_validation(*("2019-01-20", "2019-01-29"))
    Out[15]: True

    In [16]: date_validation(*("219-01-20", "2019-01-29"))
    Out[16]: False # Because first one is not valid

    In [17]: date_validation("2019-01-29")
    Out[17]: True

    In [18]: date_validation("2019-1-29")
    Out[18]: True

    In [19]: date_validation("2019-1-60")
    Out[19]: False # Day is not correct

    :param date: "2019-08-01"
    :param args: **("2019-08-01", "2019-07-20")
    :return: True or False
    :rtype: bool
    """
    try:
        if args:
            for item in args:
                datetime.datetime.strptime(item, "%Y-%m-%d")
        if date:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:

        return False
