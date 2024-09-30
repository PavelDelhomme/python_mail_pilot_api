from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Folder

@receiver(post_save, sender=User)
def create_default_folders(sender, instance, created, **kwargs):
    if created:
        Folder.objects.create(name="Réception", user=instance)
        Folder.objects.create(name="Archives", user=instance)
        Folder.objects.create(name="Corbeille", user=instance)
