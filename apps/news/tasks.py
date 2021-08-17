from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from apps.news.utils import get_newsletter_format

logger = get_task_logger(__name__)


@shared_task(name='send_newsletter')
def send_newsletter(keywords: list, data: list, email: str) -> bool:
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    for news in data:
        description = news.get('description')
        if any(map(description.__contains__, keywords)):
            message = Mail(
                from_email="Personalized News Feed",
                to_emails=email,
                subject=news['title'],
                html_content=get_newsletter_format(news['title'], news['description'], news['url']))
            sg.send(message)
            pass
    return True

