from django.urls import path
from django.conf.urls import handler404, handler500
from .views import error_404, error_500, homepage_view

handler404 = error_404
handler500 = error_500

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('404/', error_404),
    path('500/', error_500),

]