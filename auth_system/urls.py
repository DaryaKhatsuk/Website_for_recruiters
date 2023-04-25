from django.urls import path
from django.conf.urls import handler404, handler500
from django.views.defaults import page_not_found, server_error
from .views import error_404, error_500, error_frame_view, registration_view, login_view, logout_view, account_view, \
    account_verif_view, support_view, support_done_view, password_reset_view, password_reset_done_view, \
    delete_account_view, delete_account_done_view, not_delete_view

handler404 = error_404
handler500 = error_500

urlpatterns = [
    path('registration/', registration_view, name='registration'),
    path('account_verif/', account_verif_view, name='account_verif'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('account/', account_view, name='account'),

    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_done/', password_reset_done_view, name='password_reset_done'),

    path('delete_account/', delete_account_view, name='delete_account'),
    path('delete_account_done/', delete_account_done_view, name='delete_account_done'),
    path('not_delete_acc/', not_delete_view, name='not_delete_acc'),



    path('support/', support_view, name='support'),
    path('support/support_done/', support_done_view, name='support_done'),

    path('error_frame/', error_frame_view, name='error_frame'),
    path('404/', error_404),
    path('500/', error_500),
    # path(page_not_found, error_500),
    # path(server_error, error_500),
]
