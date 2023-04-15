from django import forms
from django.contrib.auth.models import User


# from .models import


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', help_text='The username must be unique and contain no spaces',
                               max_length=50, error_messages='This name is already taken', unique=True)
    name = forms.CharField(label='Name', max_length=50)
    email = forms.CharField(label='Email', max_length=155, widget=forms.EmailInput,
                            help_text='Please use a valid email address so that you can be contacted',
                            error_messages='This email address is invalid or already taken', unique=True)
    ConsentDataProcessing = forms.NullBooleanField(label='Consent to data processing')

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'ConsentDataProcessing', 'password')


class AccountVerifForm(forms.ModelForm):
    code = forms.CharField(max_length=12, label='Code')

    class Meta:
        model = User
        fields = ('code',)


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)


class ResetForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    username = forms.CharField(label='Username', max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email')


class AccountDelForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ('email',)


class AccountVerif(forms.ModelForm):
    code = forms.CharField(max_length=10, label='Code')

    class Meta:
        model = User
        fields = ('code',)


class SaveLocation(forms.ModelForm):
    selecting = forms.CharField(max_length=12, label='Selecting', choices=(('D', 'On device'), ('S', 'On server')))
    location = forms.FileField(max_length=255, label='Location', null=True, blank=True)

    class Meta:
        model = User
        fields = ('selecting', 'location')


class Language(forms.ModelForm):
    language = forms.CharField(max_length=3, label='Language', choices=(('EN', 'English'), ('RU', 'Русский')))

    class Meta:
        model = User
        fields = ('language',)

# class SupportForm(forms.ModelForm):
#     UserText = forms.CharField(max_length=2000, label='Message', widget=forms.Textarea)
#     emailUser = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput)
#
#     class Meta:
#         model = Support
#         fields = ('UserText', 'emailUser')
