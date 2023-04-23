from django import forms
from django.contrib.auth.models import User
from filebrowser.fields import FileBrowseField
from .models import AccountVerif, Language


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', help_text='The username must be unique and contain no spaces',
                               max_length=50)
    name = forms.CharField(label='Name', max_length=50)
    email = forms.CharField(label='Email', max_length=255, widget=forms.EmailInput,
                            help_text='Please use a valid email address so that you can be contacted')
    CHOICES = [('D', 'On device'), ('S', 'On server')]
    selecting = forms.TypedChoiceField(choices=CHOICES, coerce=str)
    directory = FileBrowseField('Directory', max_length=255)
    ConsentDataProcessing = forms.TypedChoiceField(label='Consent to data processing', choices=((True, 'Yes'),
                                                                                                (False, 'No')))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already taken.')
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'ConsentDataProcessing', 'password', 'selecting', 'location')


class AccountVerifForm(forms.ModelForm):
    code = forms.CharField(max_length=12, label='Code')

    class Meta:
        model = AccountVerif
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


class LanguageForm(forms.ModelForm):

    class Meta:
        model = Language
        fields = ('language',)
