"""notifications/signals.py — Cross-app notification signals."""
from django.db.models.signals import post_save
from django.dispatch import receiver


# Voice message notification
def notify_voice_message(sender, instance, created, **kwargs):
    if created:
        from .models import Notification
        Notification.objects.create(
            user=instance.receiver,
            title='🎙️ New Voice Message',
            message=f'{instance.sender.display_name} sent you a voice message!',
            notification_type='voice',
            link='/voice-messages/',
        )


# Memory notification
def notify_new_memory(sender, instance, created, **kwargs):
    if created:
        from .models import Notification
        from django.contrib.auth import get_user_model
        User = get_user_model()
        # Notify the partner
        partner = User.objects.exclude(pk=instance.created_by.pk).first() if instance.created_by else None
        if partner:
            Notification.objects.create(
                user=partner,
                title='📸 New Memory Added',
                message=f'{instance.created_by.display_name} added a new memory: "{instance.title}"',
                notification_type='memory',
                link=f'/memories/{instance.pk}/',
            )


def connect_signals():
    from voice_messages.models import VoiceMessage
    from memories.models import Memory
    post_save.connect(notify_voice_message, sender=VoiceMessage)
    post_save.connect(notify_new_memory, sender=Memory)


# Called from NotificationsConfig.ready()
connect_signals()
