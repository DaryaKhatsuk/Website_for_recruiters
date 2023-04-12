from django import forms
from django.contrib.auth.models import User
from models import Notes, Company, Currency, Candidate, Vacancy, Emails, Meetings, AppendLine, Selection, SelectionStage


class NotesForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    note = forms.CharField(max_length=1000, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Notes
        fields = ('title', 'note')

class CompanyForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=300, widget=forms.Textarea, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        model = Notes
        fields = ('name', 'website', 'description', 'industry', 'comments')

class VacancyForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100)

    class Meta:
        model = Notes
        fields = ('title', 'note')

class NotesForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    note = forms.CharField(max_length=1000, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Notes
        fields = ('title', 'note')

class NotesForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    note = forms.CharField(max_length=1000, null=True, blank=True, widget=forms.Textarea)

    class Meta:
        model = Notes
        fields = ('title', 'note')

