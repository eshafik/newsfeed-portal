from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler, RefreshJSONWebToken

from app_libs.error_codes import ERROR_CODE
from apps.user.models import User, UserPreference
from apps.user.validations import user_data_validation


class UserSignUp(APIView):
    """
        User sign up API related Class
        URL: URL: /api/v1/user/signup/
        Method: POST
    """
    @method_decorator(user_data_validation)
    def post(self, request):
        """
            :param request:
        """
        with transaction.atomic():
            user = User.objects.create_user(request.data.get('username'), request.data.get('password'))
            UserPreference.objects.create(user=user)
        return Response(data={"message": "User Created!"}, status=status.HTTP_201_CREATED)


class UserToken(ObtainJSONWebToken):
    """
    A custom class for JWT Token
        URL: /api/v1/user/token/
        Method: POST
    """
    def post(self, request, *args, **kwargs):
        """
        :param request:
        :raises
            - KEY_ERROR: mistake spelling username or password
            - VALUE_ERROR: wrong value
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)

            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (timezone.now() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response

        return Response(ERROR_CODE.global_codes.VALUE_ERROR, status=401)


class UserRefreshToken(RefreshJSONWebToken):
    """
    A custom class for JWT Refresh Token
        URL: /api/v1/user/refresh-token/
        Method: POST
    """

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param format:
        :return:
        :raises
            - KEY_ERROR: token keyword is not provided or spelling mistake
            - ALL_FIELDS_REQUIRED: empty token field
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)

            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (timezone.now() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response
        return Response(ERROR_CODE.global_codes.VALUE_ERROR, status=401)


class UserPreferenceAPI(APIView):
    """
        User Preference Update API
        URL: URL: /api/v1/user/preference/
        Method: PATCH
    """
    model_name = UserPreference

    def patch(self, request):
        user_pref_obj = self.request.user.userpreference
        pref_keys = ['country', 'source', 'key']
        data = {key: request.data[key] for key in request.data if (key in pref_keys and isinstance(key, list))}
        data and user_pref_obj.__dict__.update(data)
        return Response(data={'message': 'Preference Updated Successful'}, status=status.HTTP_200_OK)


# custom json response for page not found
def error404(request, exception):
    return JsonResponse({"Message": "Page not found", "code": "PNF404"}, status=404)
