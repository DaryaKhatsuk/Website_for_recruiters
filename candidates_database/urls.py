from django.urls import path
from django.conf.urls import handler404, handler500
from .views import homepage_view, notes_view, note_view, informs_view, companies_view, company_view, vacancies_view, \
    vacancy_view, emails_view, email_view, candidates_view, candidate_view \
    # error_frame_view

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('informs/', informs_view, name='informs'),
    path('notes/', notes_view, name='notes'),
    path('note/', note_view, name='note'),



    # path('error_frame/', error_frame_view, name='error_frame'),
    # path('404/', error_404),
    # path('500/', error_500),

]