from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import time

# Create your views here.


class ItemListView(APIView):
    def get(self, request, format=None):
        items = ['Item 1', 'Item 2', 'Item 3']
        time.sleep(2)
        return Response({'items': items})


def login_view(request):
    return render(request, 'fnk_auth/login.html')


def logout_view(request):
    return render(request, 'fnk_auth/logout.html')
