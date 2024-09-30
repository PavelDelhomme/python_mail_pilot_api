from rest_framework.decorators import api_view
from django.http import JsonResponse
from .client_file import fetch_emails
from imapclient import IMAPClient
from django.core.mail import send_mail as django_send_mail
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

@api_view(['POST'])
def login_view_email(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=400)

    try:
        # Vérification IMAP
        with IMAPClient('imap.mail.ovh.net', use_uid=True, ssl=True) as server:
            server.login(email, password)
            user, created = User.objects.get_or_create(username=email)
            if created:
                user.set_password(password)
                user.save()

            # Authentifier l'utilisateur dans Django
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Login successful"})
            else:
                return Response({"error": "Authentication failed"}, status=401)
    except Exception as e:
        print(f"Erreur : {e}")
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def get_emails(request):
    emails = fetch_emails()
    return JsonResponse(emails, safe=False)

@api_view(['POST'])
def send_mail(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    recipient_list = [request.data.get('recipient')]
    sender = request.data.get('sender')

    if subject and message and recipient_list:
        django_send_mail(
            subject=subject,
            message=message,
            from_email=sender,
            recipient_list=recipient_list,
        )
        return Response({"status": "Email sent successfully"}, status=200)
    return Response({"error": "Invalid data"}, status=400)