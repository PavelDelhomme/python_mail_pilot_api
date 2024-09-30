from django.db import models
from django.contrib.auth.models import User

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
