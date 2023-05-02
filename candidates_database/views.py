from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.i18n import set_language
from django.core.mail import EmailMessage, get_connection
from .models import AppendLine, Comments, Company, Currency, Vacancy, Emails, Candidate, Meetings, Notes, Selection, \
    SelectionStage
from .forms import AppendLineForm, SelectionStageForm, SelectionForm, CommentsForm, NotesForm, CurrencyForm, \
    CompanyForm, VacancyForm, EmailsForm, CandidateForm, MeetingsForm
# from .management.commands.emails import email_registration_email, password_reset_email, delete_account_email, \
#     support_email
from datetime import date, datetime
from site_for_HR.settings import DATETIME_LOCAL


"""
Errors
"""


# def error_404(request, exception):
#     return render(request, 'base.html', status=404)
#
#
# def error_500(request):
#     return render(request, 'base.html', status=500)
#
#
def error_frame_view(request):
    context = {
    }
    return render(request, 'errors/error_frame.html', context)


"""
Technical: AppendLine, Comments, Currency
"""


# @login_required
# def append_line_create(request):
#     form = AppendLineForm(request.POST or None)
#     if form.is_valid():
#         append_line = form.save(commit=False)
#         append_line.recruiter = request.user
#         append_line.save()
#         return redirect('company_create')
#     context = {
#         'form': form,
#     }
#     return render(request, 'append_line_create.html', context)
#
#
# @login_required
# def comments_create(request):
#     form = CommentsForm(request.POST or None)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.save()
#         return redirect('company_create')
#     context = {
#         'form': form,
#     }
#     return render(request, 'comments_create.html', context)


"""
Homepage, Notes, Note, Informs
"""


def homepage_view(request):
    try:
        context = {
            'date_local': DATETIME_LOCAL,
        }
        return render(request, 'informs/homepage.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def informs_view(request):
    try:
        context = {
        }
        return render(request, 'informs/homepage.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def notes_view(request):
    try:
        context = {
            'notes': Notes.objects.filter(recruiter=request.user).order_by('-datatime_update'),
        }
        return render(request, 'notes/notes.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def note_view(request, id_note):
    try:
        context = {
            'note': Notes.objects.filter(id=id_note, recruiter=request.user),
        }
        return render(request, 'notes/notes.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def note_form_view(request):
    try:
        if request.method == 'POST':
            form = NotesForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.recruiter = request.user
                note.datatime_create = DATETIME_LOCAL
                note.datatime_update = DATETIME_LOCAL
                note.save()
                return redirect('note', vacancy_id=note.id)
        else:
            form = NotesForm()
        context = {
            'form': NotesForm(),
        }
        return render(request, 'notes/notes.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def note_update_view(request, id_note):
    try:
        note = get_object_or_404(Notes, id=id_note, recruiter=request.user)
        if request.method == 'POST':
            form = NotesForm(request.POST, instance=note)
            if form.is_valid():
                note = form.save(commit=False)
                note.datatime_update = DATETIME_LOCAL
                note.save()
                return redirect('note', id=note.id)
        else:
            form = NotesForm(instance=note)
        context = {
            'form': NotesForm(),
        }
        return render(request, 'notes/notes.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Companies, Company, Form
"""


@login_required
def companies_view(request):
    try:
        context = {
            'companies': Company.objects.filter(recruiter=request.user).order_by('-datatime_update'),
        }
        return render(request, 'companies/companies_list.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def company_view(request, id_company):
    try:
        context = {
            'company': Company.objects.filter(id=id_company, recruiter=request.user),
        }
        return render(request, 'companies/company_card.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def company_form_view(request):
    try:
        if request.method == 'POST':
            form = CompanyForm(request.POST)
            if form.is_valid():
                company = form.save(commit=False)
                company.recruiter = request.user
                company.datatime_create = DATETIME_LOCAL
                company.datatime_update = DATETIME_LOCAL
                company.save()
                return redirect('company', vacancy_id=company.id)
        else:
            form = CompanyForm()
        context = {
            'form': CompanyForm(),
        }
        return render(request, 'companies/company_form.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def company_update_view(request, id_company):
    try:
        company = get_object_or_404(Company, id=id_company, recruiter=request.user)
        if request.method == 'POST':
            form = NotesForm(request.POST, instance=company)
            if form.is_valid():
                company = form.save(commit=False)
                company.datatime_update = DATETIME_LOCAL
                company.save()
                return redirect('company', id=company.id)
        else:
            form = CompanyForm(instance=company)
        context = {
            'form': CompanyForm(),
        }
        return render(request, 'companies/company_form.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Vacancies, Vacancy, Form
"""


@login_required
def vacancies_view(request):
    try:
        vacancies = Vacancy.objects.filter(recruiter=request.user).order_by('-datatime_update')
        context = {
            'vacancies': vacancies,
        }
        return render(request, 'vacancies/vacancies_list.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def vacancy_view(request, id_vacancy):
    try:
        vacancy = Vacancy.objects.filter(id=id_vacancy, recruiter=request.user)
        candidates = Candidate.objects.filter(vacancy=vacancy).order_by('-datatime_update')
        context = {
            'vacancy': vacancy,
            'candidates': candidates,
            'selection': Selection.objects.filter(vacancy=vacancy),
        }
        return render(request, 'vacancies/vacancy_card.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def vacancy_form_view(request):
    try:
        if request.method == 'POST':
            form = VacancyForm(request.POST)
            if form.is_valid():
                vacancy = form.save(commit=False)
                vacancy.recruiter = request.user
                vacancy.datatime_create = DATETIME_LOCAL
                vacancy.datatime_update = DATETIME_LOCAL
                vacancy.save()
                return redirect('vacancy_card', vacancy_id=vacancy.id)
        else:
            form = VacancyForm()
        context = {
            'form': VacancyForm(),
        }
        return render(request, 'vacancies/vacancy_form.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def vacancy_update(request, vacancy_id):
    try:
        vacancy = get_object_or_404(Vacancy, id=vacancy_id, recruiter=request.user)
        if request.method == 'POST':
            form = VacancyForm(request.POST, instance=vacancy)
            if form.is_valid():
                vacancy = form.save(commit=False)
                vacancy.datatime_update = DATETIME_LOCAL
                vacancy.save()
                return redirect('vacancy_card', vacancy_id=vacancy.id)
        else:
            form = VacancyForm(instance=vacancy)
        context = {
            'form': form,
        }
        return render(request, 'vacancies/vacancy_form.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Emails, Email, Form
"""


@login_required
def emails_view(request):
    try:
        context = {
            'emails': Emails.objects.filter(recruiter=request.user).order_by('-datatime_update'),
        }
        return render(request, 'messages/emails_list.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def email_view(request, id_email):
    try:
        context = {
            'email': Emails.objects.filter(id=id_email, recruiter=request.user),
        }
        return render(request, 'messages/email_card.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def email_form_view(request):
    try:
        context = {
            'form': EmailsForm(),
        }
        return render(request, 'messages/email_form.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Candidates, Candidate, Form
"""


@login_required
def candidates_view(request):
    try:
        context = {
            'candidates': Candidate.objects.filter(referred_by=request.user).order_by('-datatime_update'),
        }
        return render(request, 'candidates/candidates_list.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def candidate_view(request, id_candidate):
    try:
        context = {
            'candidate': Candidate.objects.filter(id=id_candidate, recruiter=request.user),
        }
        return render(request, 'candidates/candidate_card.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def candidate_form_view(request, vacancy_id):
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id, recruiter=request.user)
        if request.method == 'POST':
            form = CandidateForm(request.POST)
            if form.is_valid():
                candidate = form.save(commit=False)
                candidate.vacancy = vacancy
                candidate.datatime_create = DATETIME_LOCAL
                candidate.datatime_update = DATETIME_LOCAL
                candidate.save()
                return redirect('vacancy_detail', vacancy_id=vacancy.id)
        else:
            form = CandidateForm()
        context = {
            'form': CandidateForm(),
            'vacancy': vacancy
        }
        return render(request, 'candidates/candidate_form.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def candidate_update(request, vacancy_id, candidate_id):
    try:
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        candidate = get_object_or_404(Candidate, id=candidate_id, vacancy=vacancy)
        if request.method == 'POST':
            form = CandidateForm(request.POST, instance=candidate)
            if form.is_valid():
                candidate = form.save(commit=False)
                candidate.vacancy = vacancy
                candidate.datatime_update = DATETIME_LOCAL
                candidate.save()
                return redirect('vacancy_detail', vacancy_id=vacancy.id)
        else:
            form = CandidateForm(instance=candidate)
        context = {
            'vacancy': vacancy,
            'form': form,
            'action': 'Update',
        }
        return render(request, 'candidates/candidate_update.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Planning: Meetings, Meeting, Schedule
"""


@login_required
def meetings_view(request):
    try:
        context = {
            'meetings': Meetings.objects.filter(recruiter=request.user).order_by('-datatime_update'),
        }
        return render(request, '', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def meeting_view(request, id_meeting):
    try:
        context = {
            'candidate': Meetings.objects.filter(id=id_meeting, recruiter=request.user),
        }
        return render(request, 'candidates/candidate_card.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def meeting_form_view(request):
    try:
        context = {
            'form': MeetingsForm(),
        }
        return render(request, 'candidates/candidate_card.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')
