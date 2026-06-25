"""notifications/context_processors.py — Inject unread count into all templates."""
from .models import Notification


def notifications_processor(request):
    if getattr(request.user, 'is_authenticated', False):
        try:
            unread_count = Notification.objects.filter(
                user=request.user,
                is_read=False,
            ).count()
        except Exception:
            unread_count = 0
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}
