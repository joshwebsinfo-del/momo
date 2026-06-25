from django.contrib import admin

from .models import DailyCheckIn


@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_in_date', 'mood', 'created_at')
    search_fields = ('user__email', 'mood', 'note', 'gratitude')
    list_filter = ('check_in_date', 'mood')
    ordering = ('-check_in_date',)
