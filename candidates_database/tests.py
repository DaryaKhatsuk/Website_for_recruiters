from django.test import TestCase
from .models import AppendLine, Comments, Company, Currency, Vacancy
from .forms import AppendLineForm, CommentsForm, CompanyForm, CurrencyForm, VacancyForm
from django.contrib.auth.models import User


class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_AppendLine_model(self):
        append_line = AppendLine.objects.create(recruiter=self.user, name_line='Test Name', line='Test Line')
        self.assertEqual(str(append_line), 'Test Name')

    def test_Comments_model(self):
        comment = Comments.objects.create(comment='Test Comment')
        self.assertEqual(str(comment), 'Test Comment')

    def test_Company_model(self):
        company = Company.objects.create(name='Test Company', recruiter=self.user, website='www.testcompany.com',
                                         description='Test Description', industry='Test Industry')
        self.assertEqual(str(company), 'Test Company')

    def test_Currency_model(self):
        currency = Currency.objects.create(choices_lang='USD')
        self.assertEqual(str(currency), 'USD')

    def test_Vacancy_model(self):
        company = Company.objects.create(name='Test Company', recruiter=self.user, website='www.testcompany.com',
                                         description='Test Description', industry='Test Industry')
        currency = Currency.objects.create(choices_lang='USD')
        vacancy = Vacancy.objects.create(title='Test Vacancy', company=company, description='Test Description',
                                         salary_min=1000, salary_max=2000, currency=currency, location='Test Location')
        self.assertEqual(str(vacancy), 'Test Vacancy')


class FormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_AppendLine_form(self):
        form_data = {'name_line': 'Test Name', 'line': 'Test Line'}
        form = AppendLineForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_Comments_form(self):
        form_data = {'comment': 'Test Comment'}
        form = CommentsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_Currency_form(self):
        form_data = {'choices_lang': 'USD'}
        form = CurrencyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_Company_form(self):
        form_data = {'name': 'Test Company', 'website': 'www.testcompany.com', 'description': 'Test Description',
                     'industry': 'Test Industry'}
        form = CompanyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_Vacancy_form(self):
        company = Company.objects.create(name='Test Company', recruiter=self.user, website='www.testcompany.com',
                                         description='Test Description', industry='Test Industry')
        currency = Currency.objects.create(choices_lang='USD')
        form_data = {'title': 'Test Vacancy', 'company': company.pk, 'description': 'Test Description',
                     'salary_min': 1000, 'salary_max': 2000, 'currency': currency.pk, 'location': 'Test Location'}
        form = VacancyForm(data=form_data)
        self.assertTrue(form.is_valid())
