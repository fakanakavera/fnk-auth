from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate

import time


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password(request):
    user = authenticate(email=request.user.email,
                        password=request.data['oldPassword'])
    if not user:
        return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(request.data['newPassword'])
    user.save()
    return Response({'success': 'Password changed successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_email(request):
    user = request.user
    return Response({'email': user.email})


class ItemListView(APIView):
    def get(self, request, format=None):
        items = ['Item 1', 'Item 2', 'Item 3']
        time.sleep(2)
        return Response({'items': items})


# def login_view(request):
#     return render(request, 'fnk_auth/login.html')


# def logout_view(request):
#     return render(request, 'fnk_auth/logout.html')
