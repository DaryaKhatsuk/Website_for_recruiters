from django import forms
from django.contrib.auth.models import User
from .models import AccountVerif, Language, AccountDirectory, Support, SettingsUser


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', help_text='The username must be unique and contain no spaces',
                               max_length=50)
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    email = forms.CharField(label='Email', max_length=255, widget=forms.EmailInput,
                            help_text='Please use a valid email address so that you can be contacted')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class SettingsUserForm(forms.ModelForm):
    CHOICES = [('D', 'On device'), ('S', 'On server')]
    selecting = forms.TypedChoiceField(choices=CHOICES, coerce=str)
    ConsentDataProcessing = forms.TypedChoiceField(label='Consent to data processing', choices=((True, 'Yes'),
                                                                                                (False, 'No')))

    class Meta:
        model = SettingsUser
        fields = ('ConsentDataProcessing', 'selecting')


class AccountDirectoryForm(forms.ModelForm):

    class Meta:
        model = AccountVerif
        fields = ('code',)


class AccountVerifForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        if AccountVerif.objects.filter(code=code).exists():
            raise forms.ValidationError('Invalid verification code.')
        return cleaned_data

    class Meta:
        model = AccountDirectory
        fields = ('directory',)


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


class LanguageForm(forms.ModelForm):

    class Meta:
        model = Language
        fields = ('language',)


class SupportForm(forms.ModelForm):
    UserText = forms.CharField(max_length=2000, label='Message', widget=forms.Textarea)
    emailUser = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput)

    class Meta:
        model = Support
        fields = ('UserText', 'emailUser')
