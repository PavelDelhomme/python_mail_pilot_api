from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserIMAPSettings
from imapclient import IMAPClient
from cryptography.fernet import Fernet


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # L'utilisateur doit être authentifié
def configure_imap(request):
    user = request.user
    imap_email = request.data.get('imap_email')
    imap_password = request.data.get('imap_password')
    imap_host = request.data.get('imap_host', 'imap.mail.ovh.net')  # Hôte par défaut

    if not imap_email or not imap_password:
        return Response({"error": "Email and password are required"}, status=400)

    try:
        # Tester la connexion IMAP
        with IMAPClient(imap_host, use_uid=True, ssl=True) as server:
            server.login(imap_email, imap_password)

        # Si la connexion est réussie, enregistrer les paramètres
        imap_settings, _ = UserIMAPSettings.objects.get_or_create(user=user)
        imap_settings.imap_email = imap_email
        imap_settings.set_password(imap_password)
        imap_settings.imap_host = imap_host
        imap_settings.save()

        return Response({"message": "IMAP settings saved successfully."}, status=200)
    except Exception as e:
        return Response({"error": f"Failed to connect to IMAP server: {str(e)}"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_imap_settings(request):
    user = request.user
    try:
        imap_settings = UserIMAPSettings.objects.get(user=user)
        return Response({
            "imap_email": imap_settings.imap_email,
            "imap_host": imap_settings.imap_host,
        }, status=200)
    except UserIMAPSettings.DoesNotExist:
        return Response({"error": "IMAP settings not configured."}, status=404)
