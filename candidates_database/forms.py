from django import forms

from .models import Notes, Company, Currency, Comments, Candidate, Vacancy, Emails, AppendLine, SelectionStage, \
    Meetings, Selection


class AppendLineForm(forms.ModelForm):
    name_line = forms.CharField(max_length=50, label='Name line')

    class Meta:
        model = AppendLine
        fields = ('name_line', 'line')


class SelectionStageForm(forms.ModelForm):
    status = forms.CheckboxSelectMultiple()

    class Meta:
        model = SelectionStage
        fields = ('status',)


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Selection
        fields = ('candidate', 'vacancy', 'status', 'stages')


class CommentsForm(forms.ModelForm):
    comment = forms.CharField(max_length=300, required=False, widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('comment',)


class NotesForm(forms.ModelForm):
    note = forms.CharField(max_length=1024, required=False, widget=forms.Textarea)

    class Meta:
        model = Notes
        fields = ('title', 'note')


class CurrencyForm(forms.ModelForm):
    choices_currency = forms.RadioSelect(choices=('USD', 'EUR', 'BYR', 'UAH', 'RUB', 'PLN'))

    class Meta:
        model = Currency
        fields = ('choices_currency',)


class CompanyForm(forms.ModelForm):
    description = forms.CharField(max_length=300, required=False, widget=forms.Textarea)
    comments = forms.CharField(max_length=300, required=False, widget=forms.Textarea)

    class Meta:
        model = Company
        fields = ('name', 'website', 'description', 'industry', 'comments', 'append_line')


class VacancyForm(forms.ModelForm):
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    comments = forms.CharField(max_length=300, required=False, widget=forms.Textarea)

    class Meta:
        model = Vacancy
        fields = ('title', 'company', 'description', 'salary_min', 'salary_max', 'currency', 'location', 'comments',
                  'append_line')


class EmailsForm(forms.ModelForm):
    content = forms.CharField(max_length=1024, required=False, widget=forms.Textarea)

    class Meta:
        model = Emails
        fields = ('sender', 'recipient', 'title', 'content')


class CandidateForm(forms.ModelForm):
    position = forms.RadioSelect()

    class Meta:
        model = Candidate
        fields = ('full_name', 'position', 'email', 'phone', 'desired_salary', 'currency', 'location', 'resume_file',
                  'applied_vacancy', 'status', 'interview_date', 'experience', 'cover_letter', 'source',
                  'message', 'sun_emails', 'comments', 'append_line')


class MeetingsForm(forms.ModelForm):
    class Meta:
        model = Meetings
        fields = ('title', 'date', 'location', 'attendees', 'participant', 'append_line')
