from django.test import TestCase
from django.contrib.auth.models import User
from .models import AccountVerif, Language
from .forms import RegistrationForm, AccountVerifForm, LoginForm, ResetForm, AccountDelForm, LanguageForm
from django.urls import reverse
from django.contrib.auth import authenticate


class AccountVerifModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.account_verif = AccountVerif.objects.create(recruiter=self.user, code='123456', state_acc='A')

    def test_account_verif_model(self):
        self.assertEqual(str(self.account_verif), f'AccountVerif {self.account_verif.id}')
        self.assertEqual(self.account_verif.recruiter, self.user)
        self.assertEqual(self.account_verif.code, '123456')
        self.assertEqual(self.account_verif.state_acc, 'A')


class LanguageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.language = Language.objects.create(recruiter=self.user, language='EN')

    def test_language_model(self):
        self.assertEqual(str(self.language), f'Language {self.language.id}')
        self.assertEqual(self.language.recruiter, self.user)
        self.assertEqual(self.language.language, 'EN')


class RegistrationFormTestCase(TestCase):
    def test_registration_form(self):
        form_data = {
            'username': 'testuser',
            'name': 'Test User',
            'email': 'test@example.com',
            'ConsentDataProcessing': True,
            'password': 'testpassword',
            'selecting': 'D',
            'location': 'Test Location'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())


class AccountVerifFormTestCase(TestCase):
    def test_account_verif_form(self):
        form_data = {
            'code': '123456'
        }
        form = AccountVerifForm(data=form_data)
        self.assertTrue(form.is_valid())


class LoginFormTestCase(TestCase):
    def test_login_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())


class ResetFormTestCase(TestCase):
    def test_reset_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        form = ResetForm(data=form_data)
        self.assertTrue(form.is_valid())


class AccountDelFormTestCase(TestCase):
    def test_account_del_form(self):
        form_data = {
            'email': 'test@example.com'
        }
        form = AccountDelForm(data=form_data)
        self.assertTrue(form.is_valid())


class LanguageFormTestCase(TestCase):
    def test_language_form(self):
        form_data = {
            'language': 'EN'
        }
        form = LanguageForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')

    def test_error_frame_view(self):
        response = self.client.get(reverse('error_frame'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'errors/error_frame.html')

    def test_error_404(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/error_frame.html')

    def test_error_500(self):
        response = self.client.get(reverse('error_500'))
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'errors/error_frame.html')

    def test_registration_view(self):
        response = self.client.post(reverse('registration'), data={
            'name': 'Test User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass',
            'confirm_password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(authenticate(username='testuser', password='testpass'))

    def test_account_verif_view(self):
        # first, register a new user
        response = self.client.post(reverse('registration'), data={
            'name': 'Test User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass',
            'confirm_password': 'testpass',
        })

        # then, verify the account using the verification code
        account_verif = AccountVerif.objects.first()
        response = self.client.post(reverse('account_verif'), data={
            'code': account_verif.code,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(account_verif.state_acc, 'A')

    def test_login_view(self):
        # first, register a new user
        response = self.client.post(reverse('registration'), data={
            'name': 'Test User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass',
            'confirm_password': 'testpass',
        })

        # then, try to login with the same credentials
        response = self.client.post(reverse('login'), data={
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('sessionid' in self.client.cookies)

    def test_password_reset_view(self):
        # first, register a new user
        response = self.client.post(reverse('registration'), data={
            'name': 'Test User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass',
            'confirm_password': 'testpass',
        })

        # then, try to reset the password using the same email and username
        response = self.client.post(reverse('password_reset'), data={
            'email': 'testuser@example.com',
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(username='testuser').check_password('testpass'))

    def test_delete_account_view(self):
        # Create a new user
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

        # Log in as the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post('/delete_account/', {
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/delete_account_done/')

    def test_support_view(self):
        response = self.client.post('/support/', {
            'emailUser': 'testuser@example.com',
            'UserText': 'Test message'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/support_done/')
