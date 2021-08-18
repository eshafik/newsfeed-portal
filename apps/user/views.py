import random
import secrets

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler, RefreshJSONWebToken
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from app_libs.error_codes import ERROR_CODE
from apps.news.serializers import UserPreferenceSerializer
from apps.user.models import User, UserPreference
from apps.user.serializers import UserProfileSerializer
from apps.user.tasks import send_otp_paswd
from apps.user.validations import signup_data_validation, preference_data_validation, profile_data_validation, \
    otp_validation, password_forgot_validation


class UserSignUp(APIView):
    """
        User sign up API related Class
        URL: URL: /api/v1/users/signup/
        Method: POST
    """
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(signup_data_validation)
    def post(self, request):
        """
            :param request:
        """
        authenticate_pin = random.randint(1111, 9999)
        expiration_at = timezone.now() + timezone.timedelta(minutes=30)
        user = User.objects.filter(username=request.data.get('username'))
        if not user:
            with transaction.atomic():
                user = User.objects.create_user(request.data['username'],
                                                request.data['password'],
                                                email=request.data['email'],
                                                is_active=False,
                                                authenticate_pin=authenticate_pin,
                                                expiration_at=expiration_at)
                UserPreference.objects.create(user=user)
                send_otp_paswd.delay(email=user.email, username=user.username, otp=authenticate_pin,
                                     expired_at=f'{expiration_at.isoformat()}')
            return Response(data={"message": "User Created! OTP has been sent to your email"},
                            status=status.HTTP_201_CREATED)
        # check if user already active
        if user and user[0].is_active:
            return Response(data={"message": "User Already Exists!"}, status=status.HTTP_409_CONFLICT)
        # if user already created but not verified then send him/her verification email again
        user = user[0]
        user.authenticate_pin = authenticate_pin
        user.expiration_at = expiration_at
        user.save()
        send_otp_paswd.delay(email=user.email, username=user.username, otp=authenticate_pin,
                             expired_at=f'{expiration_at.isoformat()}')
        return Response(data={"message": "Please verify your email!"},
                        status=status.HTTP_200_OK)


class AccountVerificationAPI(APIView):
    """
        User sign up API related Class
        URL: URL: /api/v1/users/verified/
        Method: POST
    """
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(otp_validation)
    def post(self, request):
        now_at = timezone.now()
        users = User.objects.filter(username=request.data.get('username'))
        user = users[0]
        if not users:
            return Response(data={'message': 'User account not found!'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response(data={'message': 'User already verified!'}, status=status.HTTP_409_CONFLICT)

        if users.filter(authenticate_pin=request.data.get('otp'), expiration_at__gte=now_at, is_active=False).update(is_active=True):
            return Response(data={'message': "Account verified!"}, status=status.HTTP_200_OK)

        return Response(data={'message': 'Account verification failed! OTP is expired.'},
                        status=status.HTTP_400_BAD_REQUEST)


class PasswordForgotAPI(APIView):
    """
        User sign up API related Class
        URL: URL: /api/v1/users/forgot-password/
        Method: POST
    """
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(password_forgot_validation)
    def post(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        password_length = 6
        password = secrets.token_urlsafe(password_length)
        user.set_password(password)
        user.save()
        send_otp_paswd.delay(email=user.email, username=user.username, password=password)
        return Response(data={'message': 'Temporary password has been sent to yur email. Please check.'},
                        status=status.HTTP_200_OK)


class UserToken(ObtainJSONWebToken):
    """
    A custom class for JWT Token
        URL: /api/v1/users/token/
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
        URL: /api/v1/users/refresh-token/
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


class UserProfileAPI(APIView):
    """
        User Preference Update API
        URL: URL: /api/v1/users/profile/
        Method: GET, PATCH
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(UserProfileSerializer(self.request.user).data, status=status.HTTP_200_OK)

    @method_decorator(profile_data_validation)
    def patch(self, request):
        request_data = request.data
        password = request_data.pop('password', None)
        if password:
            user = self.request.user
            user.set_password(password)
            user.save()
        if not request_data:
            print("request_Data: ", request_data)
            return Response({'message': 'Update success'}, status=status.HTTP_200_OK)
        serializer = UserProfileSerializer(self.request.user, request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print("==================")
        return Response({'message': 'Update success'}, status=status.HTTP_200_OK)


class UserPreferenceAPI(APIView):
    """
        User Preference Update API
        URL: URL: /api/v1/users/preference/
        Method: GET, PATCH
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(UserPreferenceSerializer(self.request.user.userpreference).data, status=status.HTTP_200_OK)

    @method_decorator(preference_data_validation)
    def patch(self, request):
        user_pref_obj = self.request.user.userpreference
        print("user pref obj", user_pref_obj.__dict__)
        user_pref_obj.__dict__.update(request.data)
        user_pref_obj.save()
        print("after: ", user_pref_obj.__dict__)
        return Response(data={'message': 'Preference Updated Successful'}, status=status.HTTP_200_OK)


# custom json response for page not found
def error404(request, exception):
    return JsonResponse({"Message": "Page not found", "code": "PNF404"}, status=404)
