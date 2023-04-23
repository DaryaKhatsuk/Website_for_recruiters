from django.core.mail import EmailMessage, get_connection
from site_for_HR.settings import EMAIL_ADMIN
from django.contrib.auth.models import User
from .password_generator import create_password, create_code


def email_registration(user_email='', code='Not needed as all your information will be stored locally.\n'
                                           'Also, the platform disclaims any responsibility for the security '
                                           'of your data stored on your personal device.'):
    with get_connection() as connection:
        EmailMessage(subject='Congratulations on your registration!', body=f"Dear user, your verification code: {code}"
                                                                           f"Happy using!",
                     from_email=EMAIL_ADMIN, to=[user_email],
                     connection=connection).send()


email_registration()


