from django.urls import path

from apps.news.views import NewsFeedAPI

# Put here views here
urlpatterns = [
    path('', NewsFeedAPI.as_view()),
]