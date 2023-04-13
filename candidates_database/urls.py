from django.urls import path
from django.conf.urls import handler404, handler500
from views import error_404, error_500

handler404 = error_404
handler500 = error_500

urlpatterns = [
    path('404/', error_404),
    path('500/', error_500),
]