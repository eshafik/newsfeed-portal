from django.urls import path

from apps.user.views import (
    UserToken, UserRefreshToken,
    UserSignUp, UserPreferenceAPI,
    AccountVerificationAPI, PasswordForgotAPI,
    UserProfileAPI
    )

# Put here views here
urlpatterns = [
    path('signup/', UserSignUp.as_view()),
    path('verify/', AccountVerificationAPI.as_view()),
    path('profile/', UserProfileAPI.as_view()),
    path('forgot-password/', PasswordForgotAPI.as_view()),
    path('token/', UserToken.as_view()),
    path('refresh-token/', UserRefreshToken.as_view()),
    path('perference/', UserPreferenceAPI.as_view()),
]
