from django.urls import path
from django.conf.urls import handler404, handler500
from .views import homepage_view, notes_view, note_view, note_form_view, note_update_view, informs_view, companies_view, company_view, \
    company_form_view, vacancies_view, vacancy_view, vacancy_form_view, vacancy_update, emails_view, email_view, \
    email_form_view, candidates_view, candidate_view, \
    candidate_form_view, candidate_update, \
    error_frame_view

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('informs/', informs_view, name='informs'),

    path('notes/', notes_view, name='notes'),
    path('notes/note/', note_view, name='note'),
    path('notes/note_create/', note_form_view, name='note_form'),
    path('note/note_update/', note_update_view, name='note_update'),

    path('companies/', companies_view, name='companies'),
    path('companies/company/', company_view, name='company'),
    path('companies/company_create/', company_form_view, name='company_form'),

    path('vacancies/', vacancies_view, name='vacancies'),
    path('vacancies/vacancy/', vacancy_view, name='vacancy'),
    path('vacancies/vacancy_create/', vacancy_form_view, name='vacancy_form'),
    path('vacancies/vacancy_update/', vacancy_update, name='vacancy_update'),

    path('emails/', emails_view, name='emails'),
    path('emails/email/', email_view, name='email'),
    path('emails/email_create/', email_form_view, name='email_form'),

    path('candidates/', candidates_view, name='candidates'),
    path('candidates/candidate/', candidate_view, name='candidate'),
    path('candidates/candidate_create/', candidate_form_view, name='candidate_form'),
    path('candidates/candidate_update/', candidate_update, name='candidate_update'),

    path('error_frame/', error_frame_view, name='error_frame'),
    # path('404/', error_404),
    # path('500/', error_500),

]