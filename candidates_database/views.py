from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.i18n import set_language
from django.core.mail import EmailMessage, get_connection
from .models import Company, Currency, Vacancy, Emails, Candidate, Meetings, Notes, Selection, SelectionStage
from .forms import SelectionStageForm, SelectionForm, NotesForm, CurrencyForm, CompanyForm, VacancyForm, EmailsForm, \
    CandidateForm, MeetingsForm
# from .management.commands.emails import email_registration_email, password_reset_email, delete_account_email, \
#     support_email
from datetime import date, datetime
from site_for_HR.settings import DATETIME_LOCAL
from django.utils.translation import gettext


"""
Errors
"""


def error_404(request, exception):
    return render(request, 'base.html', status=404)


def error_500(request):
    return render(request, 'base.html', status=500)


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
#         'forms': form,
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
#         'forms': form,
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


"""
list_display
"""


@login_required
def list_display_view(request):
    # try:
    forms = {
        'notes': [Notes.objects.filter(recruiter=request.user).order_by('-datatime_update').all(),
                  'note', 'note_form'],
        'companies': [Company.objects.filter(recruiter=request.user).order_by('-datatime_update').all(),
                      'company', 'company_form'],
        'vacancies': [Vacancy.objects.filter(recruiter=request.user).order_by('-datatime_update').all(),
                      'vacancy', 'vacancy_form'],
        'emails': [Emails.objects.filter(recruiter=request.user).order_by('-sent_at').all(),
                   'email', 'email_form'],
        'candidates': [Candidate.objects.filter(referred_by=request.user).order_by('-datatime_update').all(),
                       'candidate', 'candidate_form'],
        'meetings': [Meetings.objects.filter(organizer=request.user).order_by('-datatime_update').all(),
                     'meeting', ],
    }
    form_name = request.GET.get('form')
    print('form_name', form_name)
    queryset = forms.get(form_name)
    print(queryset)
    context = {
        'forms': queryset[0],

        'content_url': f'{queryset[1]}_',

        'url_name': queryset[1],
        'add_url': queryset[2],
        'selected_type': form_name,
    }
    print(context)
    return render(request, 'candidates/list_display.html', context)
    # except Exception as ex:
    #     print(ex)
    #     return redirect('error_frame')


"""
notes
"""


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
    # try:
    print(request, id_note)
    context = {
        'note': Notes.objects.filter(id=id_note, recruiter=request.user),
    }
    return render(request, 'notes/note.html', context)
    # except Exception as ex:
    #     print(ex)
    #     return redirect('error_frame')


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
                return redirect('note', id_note=note.id)
        else:
            form = NotesForm()
        context = {
            'forms': NotesForm(),
        }
        return render(request, 'notes/note_form.html', context)
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
            'forms': NotesForm(),
        }
        return render(request, 'notes/note_update.html', context)
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
    # try:
        print(request, id_company)
        company = Company.objects.filter(id=id_company, recruiter=request.user)
        context = {
            'company': company,
        }
        return render(request, 'companies/company_card.html', context)
    # except Exception as ex:
    #     print(ex)
    #     return redirect('error_frame')


@login_required
def company_form_view(request):
    # try:
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        print(form.data)
        print(form.data.__str__())
        print(form.errors)
        if form.is_valid():
            print('form valid')
            # company = Company.objects.create(name=form.cleaned_data.get('name'),
            #                                  recruiter=request.user,
            #                                  website=form.cleaned_data.get('website'),
            #                                  description=form.cleaned_data.get('description'),
            #                                  industry=form.cleaned_data.get('industry'),
            #                                  comments=form.cleaned_data.get('comments'),
            #                                  datatime_create=DATETIME_LOCAL,
            #                                  datatime_update=DATETIME_LOCAL,)
            # company.save()
            company = form.save(commit=False)
            print(company)
            company.recruiter = request.user
            company.datatime_create = DATETIME_LOCAL
            company.datatime_update = DATETIME_LOCAL
            company.save()
            print('1:',company.id,'2:', company.name)
            return redirect('company', id_company=company.id)
    # else:
    #     form = CompanyForm()
    context = {
        'forms': CompanyForm(),
    }
    return render(request, 'companies/company_form.html', context)
    # except Exception as ex:
    #     print(ex)
    #     return redirect('error_frame')


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
            'forms': CompanyForm(),
        }
        return render(request, 'companies/company_update.html', context)
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
                return redirect('vacancy_card', id_vacancy=vacancy.id)
        else:
            form = VacancyForm()
        context = {
            'forms': VacancyForm(),
            'choices': CurrencyForm(),
        }
        return render(request, 'vacancies/vacancy_form.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


@login_required
def vacancy_update(request, id_vacancy):
    try:
        vacancy = get_object_or_404(Vacancy, id=id_vacancy, recruiter=request.user)
        if request.method == 'POST':
            form = VacancyForm(request.POST, instance=vacancy)
            if form.is_valid():
                vacancy = form.save(commit=False)
                vacancy.datatime_update = DATETIME_LOCAL
                vacancy.save()
                return redirect('vacancy_card', id_vacancy=vacancy.id)
        else:
            form = VacancyForm(instance=vacancy)
        context = {
            'forms': form,
        }
        return render(request, 'vacancies/vacancy_update.html', context)
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
            'emails': Emails.objects.filter(recruiter=request.user).order_by('-sent_at'),
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
            'forms': EmailsForm(),
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
def candidate_form_view(request):
    try:
        # vacancy = Vacancy.objects.get(recruiter=request.user)
        if request.method == 'POST':
            form = CandidateForm(request.POST)
            if form.is_valid():
                candidate = form.save(commit=False)
                # candidate.vacancy = vacancy
                candidate.datatime_create = DATETIME_LOCAL
                candidate.datatime_update = DATETIME_LOCAL
                candidate.save()
                return redirect('vacancy_detail', id_candidate=candidate.id)
        else:
            form = CandidateForm()
        context = {
            'forms': CandidateForm(),

            # 'vacancy': vacancy
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
            'forms': form,
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
            'forms': MeetingsForm(),
        }
        return render(request, 'candidates/candidate_card.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')
