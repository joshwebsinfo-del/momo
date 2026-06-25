"""accounts/admin.py"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CoupleSettings


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'profile_picture_url')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(CoupleSettings)
class CoupleSettingsAdmin(admin.ModelAdmin):
    list_display = ('couple_name', 'relationship_start_date', 'allowed_email_1', 'allowed_email_2')
    fieldsets = (
        ('Couple Identity', {'fields': ('couple_name', 'relationship_start_date', 'anniversary_date')}),
        ('Access Control', {'fields': ('allowed_email_1', 'allowed_email_2')}),
    )

    def has_add_permission(self, request):
        # Only allow one CoupleSettings record
        return not CoupleSettings.objects.exists()
