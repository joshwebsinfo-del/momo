from django.contrib import admin

from .models import PrivateMessage


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'created_at', 'is_read')
    search_fields = ('content', 'sender__email', 'receiver__email')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)
