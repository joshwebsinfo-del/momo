"""
accounts/models.py — Custom User model and Couple Settings.

Uses UUID primary keys throughout. The CoupleSettings singleton model
stores the relationship start date, allowed emails, and couple display name.
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Uses UUID as primary key and adds profile fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(blank=True, default='')
    profile_picture_url = models.URLField(
        blank=True,
        default='',
        help_text='Supabase Storage URL for profile picture'
    )

    # Use email as the primary login identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_full_name() or self.email

    @property
    def display_name(self):
        return self.first_name or self.username or self.email.split('@')[0]

    @property
    def avatar_url(self):
        """Return profile picture URL or a generated avatar."""
        if self.profile_picture_url:
            return self.profile_picture_url
        # Fallback: DiceBear avatar based on name
        name = self.display_name.replace(' ', '+')
        return f'https://api.dicebear.com/7.x/hearts/svg?seed={name}'


class CoupleSettings(models.Model):
    """
    Singleton model holding global couple configuration.
    Only one record should exist; accessed via CoupleSettings.get_settings().
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    couple_name = models.CharField(
        max_length=100,
        default='Our Love Journey',
        help_text='Display name for the couple (e.g. "Josh & Sarah")'
    )
    relationship_start_date = models.DateField(
        help_text='The date your relationship began — used for "Days Together"'
    )
    allowed_email_1 = models.EmailField(
        help_text='First approved email address for registration'
    )
    allowed_email_2 = models.EmailField(
        help_text='Second approved email address for registration'
    )
    anniversary_date = models.DateField(
        null=True,
        blank=True,
        help_text='Official anniversary date (if different from start date)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_couple_settings'
        verbose_name = 'Couple Settings'
        verbose_name_plural = 'Couple Settings'

    def __str__(self):
        return self.couple_name

    @classmethod
    def get_settings(cls):
        """Return the singleton settings record, or None if not configured."""
        return cls.objects.first()

    @property
    def allowed_emails(self):
        return [
            self.allowed_email_1.lower(),
            self.allowed_email_2.lower(),
        ]
