from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from apps.news.utils import get_newsletter_format, send_email, get_news
from apps.user.models import User

logger = get_task_logger(__name__)


@shared_task
def send_newsletter() -> bool:
    users = User.objects.filter(is_active=True, is_admin=False, is_superuser=False)
    for user in users:
        print("username", user.username)
        data = get_news(user.userpreference.country, user.userpreference.source)
        print("count: ", data)
        for news in data:
            description = news.get('description')
            title = news.get('title')
            if (any(map(description.__contains__, user.userpreference.keywords)) or any(
                    map(title.__contains__, user.userpreference.keywords))) and user.email:
                is_send, message = send_email(user.email, title, description, news['url'])
                if not is_send:
                    logger.error(f'error sending newsletter: {message}')
    return True
