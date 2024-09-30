from django.urls import path
from .views import get_mails, send_mail
from .views import manage_folders, manage_subfolders

urlpatterns = [
    path('mails/', get_mails),
    path('send/', send_mail),
    path('folders/', manage_folders),
    path('folders/<int:folder_id>/subfolders/', manage_subfolders),
]