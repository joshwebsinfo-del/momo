from django.contrib import admin

from .models import ApprovedAccount, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)


@admin.register(ApprovedAccount)
class ApprovedAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    actions = ('activate_selected', 'deactivate_selected')

    @admin.action(description='Activate selected approved emails')
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected approved emails')
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)
