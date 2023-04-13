from django.shortcuts import render


def error_404(request, exception):
    return render(request, 'base.html', status=404)


def error_500(request):
    return render(request, 'base.html', status=500)
