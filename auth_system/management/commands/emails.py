from django.core.mail import EmailMessage, get_connection
from site_for_HR.settings import EMAIL_ADMIN
from django.contrib.auth.models import User
from .password_generator import create_password, create_code


def email_registration(code='Not needed as all your information will be stored locally.\nAlso, the platform disclaims '
                            'any responsibility for the security of your data stored on your personal device.',
                       user_email='', username='', name=''):
    with get_connection() as connection:
        EmailMessage(subject='Congratulations on your registration!', body=f"Dear {name},\n your verification code: "
                                                                           f"{code}\nYour username: {username}\n"
                                                                           f"Happy using!",
                     from_email=EMAIL_ADMIN, to=[user_email],
                     connection=connection).send()


email_registration()


def password_reset(new_password='', name='', user_email='', username=''):
    with get_connection() as connection:
        EmailMessage(subject='Reset password', body=f"Dear {name} with username {username}!\nYou received this message "
                                                    f"because you requested it to be restored on the site.\n"
                                                    f"Your new password: {new_password}\n"
                                                    f"Please write it down and delete this message.",
                     from_email=EMAIL_ADMIN, to=[user_email], connection=connection).send()


password_reset()
