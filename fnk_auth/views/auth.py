from ..serializers import UserSerializer
from django.contrib.auth import authenticate
from ..views.email import send_verification_email
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
import requests


def check_recaptcha(request):
    recaptcha_response = request.data.get('recaptcha')
    if not recaptcha_response:
        print('reCAPTCHA is required')
        return Response({"detail": "reCAPTCHA is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Verify reCAPTCHA response with Google
    data = {
        'secret': '6Lc5V60pAAAAAOH1x4J8IebcDPoyb1jc4WdE__Va',
        'response': recaptcha_response
    }
    result = requests.post(
        'https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = result.json()

    if not result_json.get('success'):
        print('reCAPTCHA is invalid')
        return Response({"detail": "Invalid reCAPTCHA. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

    # Proceed with the original behavior if reCAPTCHA is valid
    return Response({'success': 'reCAPTCHA is valid'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        print(args)
        print(kwargs)
        # Check reCAPTCHA
        # if check_recaptcha(request).status_code != 200:
        #     return check_recaptcha(request)

        # Proceed with the original behavior if reCAPTCHA is valid
        return super().post(request, *args, **kwargs)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Send verification email
        email_sent = send_verification_email(user)
        if email_sent:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Email could not be sent'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
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
