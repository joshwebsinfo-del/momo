"""notes/tasks.py — Celery task for scheduled note delivery."""
from celery import shared_task
from django.utils import timezone


@shared_task
def deliver_scheduled_notes():
    """
    Periodic task: deliver all notes whose scheduled_for time has arrived.
    Run this every hour via Celery Beat.
    """
    from .models import LoveNote
    from notifications.models import Notification

    now = timezone.now()
    pending = LoveNote.objects.filter(
        scheduled_for__lte=now,
        is_delivered=False,
    )

    count = 0
    for note in pending:
        note.is_delivered = True
        note.save(update_fields=['is_delivered'])

        # Notify the receiver
        Notification.objects.create(
            user=note.receiver,
            title='💌 A scheduled note has arrived!',
            message=f'{note.sender.display_name} wrote you something special: "{note.title}"',
            notification_type='note',
            link=f'/notes/{note.pk}/',
        )
        count += 1

    return f'Delivered {count} scheduled note(s).'
