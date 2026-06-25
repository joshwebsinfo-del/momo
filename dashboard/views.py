from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'landing.html')

from checkins.models import DailyCheckIn
from countdowns.models import Countdown
from goals.models import Goal
from memories.models import Memory
from notes.models import LoveNote
from notifications.models import Notification
from timeline.models import TimelineEvent
from voice_messages.models import VoiceMessage


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        created = self.request.user.created_at.date()
        days_together = (today - created).days
        next_anniversary = date(today.year, created.month, created.day)
        if next_anniversary < today:
            next_anniversary = date(today.year + 1, created.month, created.day)

        memories = Memory.objects.order_by('-memory_date')[:4]
        notes = LoveNote.objects.filter(receiver=self.request.user).order_by('-created_at')[:4]
        goals = Goal.objects.order_by('-updated_at')[:3]
        timeline_events = TimelineEvent.objects.order_by('-event_date')[:4]
        countdowns = Countdown.objects.order_by('target_date')[:3]
        checkins = DailyCheckIn.objects.filter(user=self.request.user).order_by('-check_in_date')[:3]
        on_this_day = Memory.objects.filter(memory_date__month=today.month, memory_date__day=today.day).first()
        voice_messages = VoiceMessage.objects.filter(receiver=self.request.user).count()
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()

        context.update({
            'days_together': days_together,
            'next_anniversary': next_anniversary,
            'memories': memories,
            'notes': notes,
            'goals': goals,
            'timeline_events': timeline_events,
            'countdowns': countdowns,
            'checkins': checkins,
            'on_this_day': on_this_day,
            'voice_messages': voice_messages,
            'unread_notifications': unread_notifications,
            'stats': {
                'memories': Memory.objects.count(),
                'photos': Memory.objects.exclude(photo='').count(),
                'videos': Memory.objects.exclude(video='').count(),
                'notes': LoveNote.objects.count(),
                'voice': voice_messages,
                'timeline': TimelineEvent.objects.count(),
                'goals_completed': Goal.objects.filter(completed=True).count(),
            },
        })
        return context
