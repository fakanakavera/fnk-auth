from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import time
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view

# Create your views here.


@api_view(['POST'])
def register(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemListView(APIView):
    def get(self, request, format=None):
        items = ['Item 1', 'Item 2', 'Item 3']
        time.sleep(2)
        return Response({'items': items})


def login_view(request):
    return render(request, 'fnk_auth/login.html')


def logout_view(request):
    return render(request, 'fnk_auth/logout.html')
