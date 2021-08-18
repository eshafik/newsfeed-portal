from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from sendgrid import SendGridAPIClient, Mail

from apps.news.utils import get_newsletter_format

logger = get_task_logger(__name__)


@shared_task
def send_otp_paswd(email: str, username: str, otp: int = None, expired_at: str = None, password: str = None) -> bool:
    try:
        print("entered ======================================")
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        if otp:
            subject = 'Verify your account'
            title = f"Username: '{username}'  OTP: '{otp}' "
            description = f'After {expired_at}, your OTP will be expired'
        else:
            subject = 'Temporary password '
            title = f"Username: '{username}'  Password: '{password}' "
            description = f'After login with this password you can change your password from profile settings'
        print("data: ", settings.FROM_EMAIL, email, subject)
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=email,
            subject=subject,
            html_content=get_newsletter_format(title, description, "#"))
        sg.send(message)
        return True
    except Exception as error:
        logger.error(f"error on OTP sending: {error}")
        return False
