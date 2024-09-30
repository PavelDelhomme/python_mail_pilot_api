from django.urls import path
from .views import get_emails, send_mail, login_view_email #, manage_folders, manage_subfolders, get_mails

urlpatterns = [
    path('send/', send_mail),
    path('get_emails/', get_emails),
    path('login_with_email/', login_view_email),
]