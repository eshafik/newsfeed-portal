from django.urls import path

from apps.user.views import UserToken, UserRefreshToken, UserSignUp

# Put here views here
urlpatterns = [
]

internal_urls = [
    path('signup/', UserSignUp.as_view()),
    path('token/', UserToken.as_view()),
    path('refresh-token/', UserRefreshToken.as_view()),
]

urlpatterns += internal_urls
