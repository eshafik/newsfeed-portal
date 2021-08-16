"""
    Version: 1.0.0
    Author: MSI Shafik
"""

__all__ = [
    "ERROR_CODE"
]


class GlobalErrorCodes(object):
    """
    A set of constants representing validation errors.  Validation error messages can change, but the codes will not.
    See the source for a list of all errors codes.
    Codes can be used to check for specific validation errors
    """
    KEY_ERROR = dict(error_code="KE400", message="Key error")
    ALL_FIELDS_REQUIRED = dict(error_code="AFR400", message='All fields are required')
    VALUE_ERROR = dict(error_code="VE400", message="Value error")
    INVALID_REQUEST = dict(error_code="IR400", message="Invalid request")


class HTTPErrorCodes(object):
    """
    A set of constants representing validation errors.  Validation error messages can change, but the codes will not.
    See the source for a list of all errors codes.
    Codes can be used to check for specific validation errors
    """
    NETWORK_ERROR = dict(error_code="NE503", message="Network error")


class AuthenticationErrorCodes(object):
    """default_auto_field = 'django.db.models.BigAutoField'
    A set of constants representing validation errors.  Validation error messages can change, but the codes will not.
    See the source for a list of all errors codes.
    Codes can be used to check for specific validation errors
    """
    TOKEN_FAILED = dict(error_code="UTF400", message="Token generate is failed")
    TOKEN_EXPIRED = dict(error_code="UTE401", message="Token has expired.")
    TOKEN_INVALID = dict(error_code="UTI401", message="Token Invalid.")
    USER_ACCOUNT_DEACTIVATED = dict(error_code="UAD400", message="Account is deactivated")
    USER_ACCOUNT_BLOCKED = dict(error_code="UAB400", message="Account is blocked")
    USER_INVALID_CREDENTIALS = dict(error_code="UIC400", message="Invalid credentials")
    NO_CREDENTIALS_PROVIDED = dict(error_code="UNCP401", message="No credentials provided")
    USER_NOT_FOUND = dict(error_code="UNF404", message="User not found", is_exists=False)


class ErrorCodes(object):

    def __init__(self):
        self.global_codes = GlobalErrorCodes
        self.http_codes = HTTPErrorCodes
        self.authentication_codes = AuthenticationErrorCodes


# created instance
ERROR_CODE = ErrorCodes()
