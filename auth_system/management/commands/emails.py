from django.core.mail import EmailMessage, get_connection
from site_for_HR.settings import EMAIL_ADMIN
from django.contrib.auth.models import User
from .password_generator import create_password, create_code


def email_registration_email(code='Not needed as all your information will be stored locally.\nAlso, the platform disclaims '
                            'any responsibility for the security of your data stored on your personal device.',
                       user_email='', username='', name=''):
    with get_connection() as connection:
        EmailMessage(subject='Congratulations on your registration!', body=f"Dear {name},\n your verification code: "
                                                                           f"{code}\n\nYour username: {username}\n"
                                                                           f"\nHappy using!",
                     from_email=EMAIL_ADMIN, to=[user_email],
                     connection=connection).send()


email_registration_email()


def password_reset_email(new_password='', name='', user_email='', username=''):
    with get_connection() as connection:
        EmailMessage(subject='Reset password', body=f"Dear {name} with username {username}!\nYou received this message "
                                                    f"because you requested it to be restored on the site.\n"
                                                    f"Your new password: {new_password}\n"
                                                    f"Please write it down and delete this message.",
                     from_email=EMAIL_ADMIN, to=[user_email], connection=connection).send()


password_reset_email()


def delete_account_email(user_email='', name=''):
    with get_connection() as connection:
        EmailMessage(subject='Delete account', body=f"Dear {name}, your account was deleted.",
                     from_email=EMAIL_ADMIN, to=[user_email], connection=connection).send()


delete_account_email()


def support_email(date='', email='', message='', user='', cookies='', meta=''):
    with get_connection() as connection:
        EmailMessage(subject='Need support for User', body=f"Date: {date}\n"
                                                           f"Email: {email}\n"
                                                           f"Message: {message}\n"
                                                           f"Request User: {user}\n"
                                                           f"Request COOKIES: {cookies}\n"
                                                           f"Request META: {meta}\n",
                     from_email=EMAIL_ADMIN, to=[EMAIL_ADMIN],
                     connection=connection).send()


delete_account_email()



