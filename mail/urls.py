from django.urls import path
from .views import configure_imap, get_imap_settings

urlpatterns = [
    path('configure_imap/', configure_imap, name='configure_imap'),
    path('get_imap_settings/', get_imap_settings, name='get_imap_settings'),
]
