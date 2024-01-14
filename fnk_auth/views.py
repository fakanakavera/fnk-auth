from .models import UserAccountDetails
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib.auth import get_user_model

import time


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
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_nickname(request):
    user = request.user
    user_account_details = UserAccountDetails.objects.get_or_create(
        user=user)[0]
    user_account_details.nick_name = request.data['nickname']
    user_account_details.save()
    return Response({'success': 'Nickname changed successfully'})


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


def send_email(subject, message, recipient_email):
    sender_email = settings.EMAIL_HOST_USER
    sender_password = settings.EMAIL_HOST_PASSWORD
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Create a secure SSL context
        context = smtplib.SMTP(smtp_server, smtp_port)
        context.starttls()
        context.login(sender_email, sender_password)
        context.sendmail(sender_email, recipient_email, msg.as_string())
        context.quit()
        return True

    except Exception as e:
        print(e)
        return False


def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    subject = 'Verify your account'
    message = render_to_string('email_body.txt', {
        'user': user,
        'uid': uid,
        'token': token,
    })
    return send_email(subject, message, user.email)


def email_verify(request, uidb64, token):
    try:
        # Decode the uid
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(get_user_model(), pk=uid)

        # Verify the token
        if default_token_generator.check_token(user, token):
            # Perform the email verification logic
            # For example, you might want to set a flag on the user model
            user.email_verified = True  # assuming you have an email_verified field
            user.save()

            return HttpResponse("""
                <html>
                    <head>
                        <script type="text/javascript">
                            window.location.href = "http://localhost:3000/items"; // Replace with your React app's URL
                        </script>
                    </head>
                    <body>
                        If you are not redirected automatically, <a href="http://localhost:3000/items">click here</a>.
                    </body>
                </html>
                """)
        else:
            return HttpResponse("Invalid verification link")

    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
        return HttpResponse("Invalid verification link")


class ItemListView(APIView):
    def get(self, request, format=None):
        items = ['Item 1', 'Item 2', 'Item 3']
        time.sleep(2)
        return Response({'items': items})


# def login_view(request):
#     return render(request, 'fnk_auth/login.html')


# def logout_view(request):
#     return render(request, 'fnk_auth/logout.html')
