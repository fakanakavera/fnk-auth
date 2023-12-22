from django.shortcuts import render

# Create your views here.


def login_view(request):
    return render(request, 'fnk_auth/login.html')


def logout_view(request):
    return render(request, 'fnk_auth/logout.html')
