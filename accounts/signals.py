"""accounts/signals.py"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Perform any post-creation setup for new users."""
    if created:
        pass  # Future: send welcome email, create default preferences, etc.
