from django.contrib import admin
from .models import Mail, Folder

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'user')
    search_fields = ['name', 'user__username']
    list_filter = ['user']

class MailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'date_received', 'is_read', 'folder')
    search_fields = ['subject', 'sender', 'recipient']
    list_filter = ['is_read', 'folder']
    date_hierarchy = 'date_received'

admin.site.register(Folder, FolderAdmin)
admin.site.register(Mail, MailAdmin)
