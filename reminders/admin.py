from django.contrib import admin

from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'reminder_date', 'is_done', 'created_at')
    search_fields = ('title', 'note', 'user__email')
    list_filter = ('is_done', 'reminder_date')
    ordering = ('reminder_date', 'title')
