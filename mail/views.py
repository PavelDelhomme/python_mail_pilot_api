from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import UserIMAPSettings
from .client_file import fetch_emails
from imapclient import IMAPClient
from rest_framework_simplejwt.tokens import RefreshToken
from cryptography.fernet import Fernet
from django.conf import settings



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

                # Stocker les informations IMAP de façon chiffrée
                imap_settings, _ = UserIMAPSettings.objects.get_or_create(user=user)
                imap_settings.imap_email = email
                imap_settings.set_password(password)
                imap_settings.imap_host = 'imap.mail.ovh.net'
                imap_settings.save()

                # Générer un token JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
            else:
                return Response({"error": "Authentication failed"}, status=401)
    except Exception as e:
        print(f"Erreur : {e}")
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_emails(request):
    user = request.user
    try:
        imap_settings = UserIMAPSettings.objects.get(user=user)
        email = imap_settings.imap_email
        password = imap_settings.get_password()

        # Récupérer les emails
        emails = fetch_emails(email, password)
        return JsonResponse(emails, safe=False)
    except UserIMAPSettings.DoesNotExist:
        return Response({"error": "IMAP settings not configured."}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
