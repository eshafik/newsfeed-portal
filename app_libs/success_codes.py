"""
    Version: 1.0.0
    Author: MSI Shafik
"""

__all__ = [
    "SUCCESS_CODE"
]


class GlobalSuccessCodes(object):
    """
    A set of constants representing validation errors.  Validation error messages can change, but the codes will not.
    See the source for a list of all errors codes.
    Codes can be used to check for specific validation errors
    """
    REQUEST_SUCCESS = dict(success_code="RS200", message="Request success")
    DATA_CREATED = dict(success_code='DC201', message="Data is created")


class AuthenticationSuccessCodes(object):
    """
    A set of constants representing validation errors.  Validation error messages can change, but the codes will not.
    See the source for a list of all errors codes.
    Codes can be used to check for specific validation errors
    """
    TOKEN_SUCCESS = dict(success_code="UTS200", message="Token success")


class SuccessCodes(object):

    def __init__(self):
        self.global_codes = GlobalSuccessCodes
        self.authentication = AuthenticationSuccessCodes


# created instance
SUCCESS_CODE = SuccessCodes()
