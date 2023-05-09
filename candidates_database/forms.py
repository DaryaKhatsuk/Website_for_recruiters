from django import forms

from .models import Notes, Company, Currency, Candidate, Vacancy, Emails, SelectionStage, \
    Meetings, Selection


class SelectionStageForm(forms.ModelForm):
    class Meta:
        model = SelectionStage
        fields = ('status',)


class SelectionForm(forms.ModelForm):
    stages = forms.ModelMultipleChoiceField(queryset=SelectionStage.objects.all(),
                                            widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Selection
        fields = ('candidate', 'vacancy', 'status', 'stages')


class NotesForm(forms.ModelForm):
    note = forms.CharField(max_length=1024, required=False, widget=forms.Textarea)

    class Meta:
        model = Notes
        fields = ('title', 'note')


class CurrencyForm(forms.ModelForm):
    choices_currency = forms.TypedChoiceField(choices=(('U', 'USD'), ('E', 'EUR'), ('B', 'BYR'), ('UA', 'UAH'),
                                                       ('R', 'RUB'), ('P', 'PLN')))

    class Meta:
        model = Currency
        fields = ('choices_currency',)


class CompanyForm(forms.ModelForm):
    description = forms.CharField(max_length=300, required=False, widget=forms.Textarea)
    comments = forms.CharField(max_length=300, required=False, widget=forms.Textarea)

    class Meta:
        model = Company
        fields = ('name', 'website', 'description', 'industry', 'comments')


class VacancyForm(forms.ModelForm):
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    comments = forms.CharField(max_length=300, required=False, widget=forms.Textarea)
    currency = forms.TypedChoiceField(choices=(('U', 'USD'), ('E', 'EUR'), ('B', 'BYR'), ('UA', 'UAH'),
                                               ('R', 'RUB'), ('P', 'PLN')))

    class Meta:
        model = Vacancy
        fields = ('title', 'company', 'description', 'salary_min', 'salary_max', 'currency', 'location', 'comments')


class EmailsForm(forms.ModelForm):
    content = forms.CharField(max_length=1024, required=False, widget=forms.Textarea)

    class Meta:
        model = Emails
        fields = ('recipient', 'title', 'content')


class CandidateForm(forms.ModelForm):
    position = forms.CharField(max_length=200)
    comments = forms.CharField(max_length=300, required=False, widget=forms.Textarea)
    cover_letter = forms.CharField(max_length=1000, required=False, widget=forms.Textarea)

    class Meta:
        model = Candidate
        fields = ('full_name', 'position', 'email', 'phone', 'desired_salary', 'currency', 'location', 'resume_file',
                  'applied_vacancy', 'status', 'experience', 'cover_letter', 'source', 'comments')


class MeetingsForm(forms.ModelForm):
    class Meta:
        model = Meetings
        fields = ('title', 'date', 'location', 'attendees', 'participant')
