from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from app_libs.custom_pagination import CustomPagination
from apps.news.utils import get_news


class NewsFeedAPI(APIView):
    """
        News Feed APIView for User
        URL:/api/v1/news
        Method: GET
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        news = get_news(countries=self.request.user.userpreference.country,
                        source=self.request.user.userpreference.source)
        if not news:
            return Response(data={"message": "Data not found! You have to set your country and source preference."},
                            status=status.HTTP_404_NOT_FOUND)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(news, request)
        return paginator.get_paginated_response(page)
