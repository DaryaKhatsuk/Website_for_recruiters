from django import forms

from models import Notes, Company, Currency, Comments, Candidate, Vacancy, Emails, AppendLine, SelectionStage


class AppendLineForm(forms.ModelForm):
    name_line = forms.CharField(max_length=50, label='Name line')

    class Meta:
        model = AppendLine
        fields = ('name_line', 'line')


class SelectionStageForm(forms.ModelForm):
    name = forms.CheckboxSelectMultiple(choices=('Candidate Selection', 'Screening interview', 'Test', 'Interview',
                                                 'Offer', 'Accepted offer', 'Exit to work'))

    class Meta:
        model = SelectionStage
        fields = ('name',)


class CommentsForm(forms.ModelForm):
    comment = forms.CharField(max_length=300, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('comment',)


class NotesForm(forms.ModelForm):
    note = forms.CharField(max_length=1024, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Notes
        fields = ('title', 'note')


class CurrencyForm(forms.ModelForm):
    choices_lang = forms.RadioSelect(choices=('USD', 'EUR', 'BYR', 'UAH', 'RUB', 'PLN'))

    class Meta:
        model = Currency
        fields = ('choices_lang',)


class CompanyForm(forms.ModelForm):
    description = forms.CharField(max_length=300, null=True, blank=True, widget=forms.Textarea)
    comments = forms.CharField(max_length=300, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Company
        fields = ('name', 'website', 'description', 'industry', 'comments', 'append_line')


class VacancyForm(forms.ModelForm):
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    comments = forms.CharField(max_length=300, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Vacancy
        fields = ('title', 'company', 'description', 'salary_min', 'salary_max', 'currency', 'location', 'comments',
                  'append_line')


class EmailsForm(forms.ModelForm):
    content = forms.CharField(max_length=1024, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Emails
        fields = ('sender', 'recipient', 'title', 'content', 'sent_at')


class CandidateForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    note = forms.CharField(max_length=1000, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Candidate
        fields = ('title', 'note')
