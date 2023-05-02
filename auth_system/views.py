from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.i18n import set_language
from django.core.mail import EmailMessage, get_connection
from .models import AccountVerif, Language, SettingsUser
from .forms import RegistrationForm, AccountVerifForm, LoginForm, ResetForm, AccountDelForm, LanguageForm, SupportForm, \
    SettingsUserForm
from .management.commands.password_generator import create_password, create_code
from .management.commands.emails import email_registration_email, password_reset_email, delete_account_email, \
    support_email
from datetime import date, datetime, timedelta
from site_for_HR.settings import DATETIME_LOCAL

"""
Errors
"""


def error_frame_view(request):
    context = {
    }
    return render(request, 'errors/error_frame.html', context)


def error_404(request, exception):
    return render(request, 'errors/error_frame.html', status=404)


def error_500(request):
    return render(request, 'errors/error_frame.html', status=500)


"""
Registration, verification, login, logout
"""


def registration_view(request):
    try:
        if request.method == 'POST':
            user_form = RegistrationForm(data=request.POST)
            print(user_form.data.__str__())
            print(user_form.errors)
            if user_form.is_valid():
                print(user_form.cleaned_data)
                username_base = User.objects.filter(username=user_form.cleaned_data.get('username')).exists()
                email_base = User.objects.filter(email=user_form.cleaned_data.get('email')).exists()
                if username_base is False and email_base is False:
                    user = User.objects.create_user(username=user_form.cleaned_data.get('username'),
                                                    first_name=user_form.cleaned_data.get('first_name'),
                                                    last_name=user_form.cleaned_data.get('last_name'),
                                                    email=user_form.cleaned_data.get('email'),
                                                    password=user_form.cleaned_data.get('password'),
                                                    )
                    print(user)
                    user_auth = authenticate(username=user_form.cleaned_data.get('username'),
                                             password=user_form.cleaned_data.get('password'),
                                             )
                    login(request, user_auth)
                    code = create_code()
                    verf = AccountVerif(recruiter=user,
                                        code=code,
                                        state_acc='U',
                                        datatime_finished=DATETIME_LOCAL.now() + timedelta(days=1),
                                        )
                    print(verf)
                    verf.save()
                    email_registration_email(user_email=user.email, code=code, username=user.username,
                                             name=f'{user.first_name, user.last_name}')
                    return redirect('account_verif')
        context = {
            'form_registration': RegistrationForm(),
        }
        return render(request, 'accounts/registration.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def account_verif_view(request):
    try:
        if request.method == 'POST':
            user_form = AccountVerifForm(data=request.POST)
            print(user_form.data.__str__())
            print(user_form.errors)
            user = request.user
            verification_code = user_form.cleaned_data['code']
            # Check if the verification code matches the one in the database
            try:
                account_verif = AccountVerif.objects.get(recruiter=user, code=verification_code,
                                                         state_acc='U')
                # print(DATETIME_LOCAL)
                # print(account_verif.datatime_finished)
                # date_l = DATETIME_LOCAL.astimezone()
                # if date_l < account_verif.datatime_finished():
                account_verif.state_acc = 'A'
                account_verif.save()
                return redirect('account')
            except AccountVerif.DoesNotExist:
                user_form.add_error('code', 'Invalid verification code.')
        context = {
            'form': AccountVerifForm(),
        }
        return render(request, 'accounts/account_verif.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def login_view(request):
    try:
        if request.method == "POST":
            user_form = RegistrationForm(data=request.POST)
            print(user_form.data.__str__())
            print(user_form.errors)
            user = authenticate(username=user_form.data.get('username'),
                                password=user_form.data.get('password'))
            login(request, user)
            return redirect('homepage')
        context = {
            'user': request.user,
            'form': LoginForm(),
        }
        return render(request, 'accounts/login.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def account_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/account.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def logout_view(request):
    logout(request)
    return redirect('homepage')


"""
Password reset view
"""


def password_reset_view(request):
    try:
        if request.method == "POST":
            user_form = ResetForm(data=request.POST)
            user_chek = user_form.data.get  # сокращение для более удобного ввода в сравнение
            try:
                user = User.objects.get(email=user_chek('email'), username=user_chek('username'))
                print(user)
                new_password = create_password()
                user.password = new_password
                user.save()
                password_reset_email(new_password, user.first_name, user.email, user.username)
                return redirect('password_reset_done')
            except AccountVerif.DoesNotExist:
                user_form.add_error('code', 'Invalid verification code.')
        context = {
            'form': ResetForm(),
        }
        return render(request, 'accounts/password_reset/password_reset.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def password_reset_done_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/password_reset/password_reset_done.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Delete account
"""


@login_required
def delete_account_view(request):
    try:
        if request.method == "POST":
            user_form = AccountDelForm(data=request.POST)
            if user_form.is_valid() and user_form.data.get('email') == request.user.email:
                user = User.objects.get(id=request.user.id)
                delete_account_email(user_email=user.email, name=user.first_name)
                user.delete()
                return redirect('delete_account_done')
            else:
                return redirect('not_delete_acc')
        context = {
            'form': AccountDelForm(),
        }
        return render(request, 'accounts/delete_account/delete_account.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def delete_account_done_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/delete_account/delete_account_done.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def not_delete_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/delete_account/not_delete.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Support
"""


def support_view(request):
    try:
        if request.method == 'POST':
            support_form = SupportForm(data=request.POST)
            if support_form.is_valid():
                support_email(date.today(), support_form.data.get('emailUser'), support_form.data.get('UserText'),
                              request.user, request.COOKIES, request.META)
                return redirect('support_done')
        context = {
            'form': SupportForm(),
        }
        return render(request, 'support/support.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def support_done_view(request):
    try:
        context = {
        }
        return render(request, 'support/support_done.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')
