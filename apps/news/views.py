from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_libs.custom_pagination import CustomPagination
from app_libs.error_codes import ERROR_CODE
from apps.news.utils import get_news
from apps.user.models import UserPreference
from apps.news.tasks import send_newsletter


class NewsFeedAPI(APIView):
    """
        News Feed APIView for User
    """
    permission_classes = ()

    def get(self, request):
        news = get_news(countries=self.request.user.userpreference.country,
                        source=self.request.user.userpreference.source)
        print("count: ", len(news))
        if not news:
            return Response(data={"message": "Data not found! You have to set your country and source preference."}, status=status.HTTP_404_NOT_FOUND)
        # self.request.user.email and send_newsletter.delay(keywords=self.request.user.userpreference.keywords,
        #                                                   data=news, email=self.request.user.email)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(news, request)
        return paginator.get_paginated_response(page)
