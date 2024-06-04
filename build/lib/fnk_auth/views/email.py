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
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator


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
    print(f"user.pk: {user.pk}")
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    subject = 'Verify your account'
    message = render_to_string('fnk_auth/email_body.txt', {
        'user': user,
        'uid': uid,
        'token': token,
    })
    return send_email(subject, message, user.email)


def email_verify(request, uidb64, token):
    try:
        # Decode the uid
        print("email_verify")
        uid = urlsafe_base64_decode(uidb64).decode()
        print(f"uid: {uid}")
        user = get_object_or_404(get_user_model(), pk=uid)
        print(f"user: {user}")
        # Verify the token
        if default_token_generator.check_token(user, token):
            # Perform the email verification logic
            # For example, you might want to set a flag on the user model
            user.email_verified = True  # assuming you have an email_verified field
            user.save()

            return HttpResponse("""
                <html>
                    <head>
                        <title>Email Verification</title>
                    </head>
                    <body>
                        <h1>Email Verification Successful</h1>
                        <p>Your email has been successfully verified. You can close this page now.</p>
                    </body>
                </html>
            """)
        else:
            return HttpResponse("Invalid verification link")

    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
        return HttpResponse("Invalid verification link")
