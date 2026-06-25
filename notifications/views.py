"""notifications/views.py"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator

from .models import Notification


@method_decorator(login_required, name='dispatch')
class NotificationListView(View):
    template_name = 'notifications/list.html'

    def get(self, request):
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')[:50]
        # Mark all as read on open
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return render(request, self.template_name, {'notifications': notifications})


@method_decorator(login_required, name='dispatch')
class MarkReadView(View):
    """AJAX endpoint to mark a notification as read."""
    def post(self, request, pk):
        notif = get_object_or_404(Notification, pk=pk, user=request.user)
        notif.is_read = True
        notif.save(update_fields=['is_read'])
        return JsonResponse({'success': True})


@method_decorator(login_required, name='dispatch')
class UnreadCountView(View):
    """AJAX endpoint returning unread count for badge polling."""
    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'count': count})


@method_decorator(login_required, name='dispatch')
class ClearAllView(View):
    def post(self, request):
        Notification.objects.filter(user=request.user).update(is_read=True)
        return redirect('notifications:list')
