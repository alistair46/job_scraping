from django.core.mail import EmailMessage
from django.core.mail import send_mail
from Backend import settings


class util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']],
        )
        email.send()