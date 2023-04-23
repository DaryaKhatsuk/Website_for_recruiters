from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage, get_connection
from .models import AccountVerif, Language
from site_for_HR.settings import EMAIL_ADMIN
from .forms import RegistrationForm, AccountVerifForm, LoginForm, ResetForm, AccountDelForm, LanguageForm
from .management.commands.password_generator import create_password, create_code
from .management.commands.emails import email_registration
from datetime import date, datetime


"""
Errors
"""


def error_frame_view(request):
    context = {
    }
    return render(request, 'errors/error_frame.html', context)


def error_404(request, exception):
    return render(request, 'base.html', status=404)


def error_500(request):
    return render(request, 'base.html', status=500)


"""
Password reset view
"""


# def password_reset_view(request):
#     try:
#         if request.method == "POST":
#             user_form = ResetForm(data=request.POST)
#             coun_users = 1
#             user_chek = user_form.data.get  # сокращение для более удобного ввода в сравнение
#             for i in User.objects.values('id', 'email', 'username', 'first_name'):
#                 # сравнение email и username отправленные пользователем с базой
#                 if user_chek('email') == i.get('email') and user_chek('username') == i.get('username'):
#                     with get_connection() as connection:
#                         new_password = create()
#                         EmailMessage(subject='Reset password', body=f"Dear {i.get('first_name')}!\n"
#                                                                     f"Your new password: {new_password}\n"
#                                                                     f"Please write it down and delete this message.",
#                                      from_email=FORM_EMAIL, to=[i.get('email')], connection=connection).send()
#                         set_user = User.objects.get(username=user_chek('username'))
#                         set_user.set_password(new_password)
#                         set_user.save()
#
#                         print(f"Пользователь с id и username: {i.get('id'), user_chek('username')}, сменил пароль")
#
#                     return redirect('password_reset_done')
#                 # только если coun_users будет равно количеству записей в базе и до этого не найдется запись,
#                 # выходит экран ошибки
#                 elif coun_users == len(User.objects.all()):
#                     return redirect('error_frame')
#                 coun_users += 1
#         context = {
#             'form': ResetForm(),
#         }
#         return render(request, 'accounts/password_reset/password_reset.html', context)
#     except Exception as ex:
#         print(ex)
#         return redirect('error_frame')
#
#
# def password_reset_done_view(request):
#     try:
#         context = {
#         }
#         return render(request, 'accounts/password_reset/password_reset_done.html', context)
#     except Exception as ex:
#         print(ex)
#         return redirect('error_frame')


"""
Registration, verification, login, logout
"""


def registration_view(request):
    try:
        if request.method == 'POST':
            user_form = RegistrationForm(data=request.POST)
            if user_form.is_valid():
                # coun_users = 1
                # for i in User.objects.values('email'):
                    # только если coun_users будет равно количеству записей в базе и до этого не найдется запись
                    # об искомом email, email будет зарегистрирован
                    # if coun_users == len(User.objects.all()) and user_form.data.get('email') != i.get('email'):
                print(user_form.cleaned_data)
                User.objects.create_user(**user_form.cleaned_data)
                # User.objects.create_user(username=user_form.cleaned_data.get('username'),
                #                          name=user_form.cleaned_data.get('name'),
                #                          email=user_form.cleaned_data.get('email'),
                #                          password=user_form.cleaned_data.get('password'),
                #                          selecting=user_form.cleaned_data.get('selecting'),
                #                          location=user_form.cleaned_data.get('location'),
                #                          ConsentDataProcessing=user_form.cleaned_data.get('ConsentDataProcessing'),
                #                          )
                user = authenticate(username=user_form.cleaned_data.get('username'),
                                    password=user_form.cleaned_data.get('password'),
                                    )
                login(request, user)
                if user_form.cleaned_data.get('selecting') == 'S':
                    email_registration(user_email=user_form.cleaned_data.get('email'))
                    return redirect('homepage')
                else:
                    # with get_connection() as connection:
                    code = create_code()
                    verf = AccountVerif(recruiter=request.user.id,
                                        code=code,
                                        state_acc='U',
                                        )
                    verf.save()

                    # EmailMessage(subject='Delete account', body=f"Dear user, your verification code: {code}"
                    #                                             f"Happy using!",
                    #              from_email=EMAIL_ADMIN, to=[user_form.cleaned_data.get('email')],
                    #              connection=connection).send()
                    # user = User.objects.get(id=request.user.id)
                    email_registration(user_email=user_form.cleaned_data.get('email'), code=code)
                    return redirect('account_verif')
                        # elif user_form.data.get('email') == i.get('email'):
                        #     return redirect('error_frame_registration')
                        # coun_users += 1

        context = {
            'form': RegistrationForm(),
        }
        return render(request, 'accounts/registration.html', context)
    # except AttributeError as ae:
    #     print(ae)
    #     return redirect('error_frame_registration')
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def account_verif_view(request):
    try:
        if request.method == 'POST':
            user_form = AccountVerifForm(data=request.POST)
            if user_form.is_valid() and AccountVerif.code == user_form.cleaned_data.get('code'):
                verf = AccountVerif(state_acc='A',
                                    )
                verf.save()
                return redirect('homepage')
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
            user = authenticate(username=user_form.data.get('username'),
                                password=user_form.data.get('password'))
            login(request, user)
            return redirect('homepage')
        context = {
            'user': request.user,
            'form': LoginForm(),
        }
        return render(request, 'accounts/account.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


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
Delete account
"""


# def delete_account_view(request):
#     try:
#         if request.method == "POST":
#             user_form = AccountDelForm(data=request.POST)
#             if Purchase.objects.filter(currentCustomer=request.user.id):
#                 return redirect('not_delete')
#             else:
#                 if user_form.is_valid() and user_form.data.get('email') == request.user.email:
#                     with get_connection() as connection:
#                         EmailMessage(subject='Delete account', body=f"Dear {request.user.first_name}, your account on "
#                                                                     f"PlortShop.Zz as deleted.",
#                                      from_email=FORM_EMAIL, to=[request.user.email], connection=connection).send()
#                         user = User.objects.get(id=request.user.id)
#                         user.delete()
#                         return redirect('delete_account_done')
#         context = {
#             'form': AccountDelForm(),
#         }
#         return render(request, 'accounts/delete_account/delete_account.html', context)
#     except Exception as ex:
#         print(ex)
#         return redirect('error_frame')
#
#
# def delete_account_done_view(request):
#     try:
#         context = {
#         }
#         return render(request, 'accounts/delete_account/delete_account_done.html', context)
#     except Exception as ex:
#         print(ex)
#         return redirect('error_frame')
#
#
# def not_delete_view(request):
#     try:
#         context = {
#         }
#         return render(request, 'accounts/delete_account/not_delete.html', context)
#     except Exception as ex:
#         print(ex)
#         return redirect('error_frame')


"""
Support
"""


def support_view(request):
    try:
        # if request.method == 'POST':
        #     support_form = SupportForm(data=request.POST)
        #     if support_form.is_valid():
        #         supportBase = Support(emailUser=support_form.data.get('emailUser'),
        #                               UserText=support_form.data.get('UserText'),
        #                               )
        #         supportBase.save()
        #         print(supportBase.idSupport)
        #         with get_connection() as connection:
        #             EmailMessage(subject='Need support', body=f"Date: {date.today()}\n"
        #                                                       f"Email: {support_form.data.get('emailUser')}\n"
        #                                                       f"Message: {support_form.data.get('UserText')}",
        #                          from_email=EMAIL_ADMIN, to=[EMAIL_ADMIN],
        #                          connection=connection).send()
        #             return redirect('support_done')
        context = {
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
