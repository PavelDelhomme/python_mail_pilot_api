from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings


class UserIMAPSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imap_email = models.EmailField()
    encrypted_password = models.BinaryField()  # Champ pour stocker le mot de passe chiffré
    imap_host = models.CharField(max_length=255)

    def set_password(self, raw_password):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        self.encrypted_password = fernet.encrypt(raw_password.encode())

    def get_password(self):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        return fernet.decrypt(self.encrypted_password).decode()


class Mail(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    recipient = models.EmailField()
    body = models.TextField()
    date_received = models.DateTimeField(auto_now_add=True)
    date_sended = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    folder = models.ForeignKey("Folder", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.sender} ({self.folder.name})"

class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Sous-dossier de : {self.parent.name if self.parent else 'Aucun'})"
