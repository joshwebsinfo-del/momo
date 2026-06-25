"""dashboard/views.py — Main dashboard and landing page views."""
from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.utils import timezone

from accounts.models import CoupleSettings
from memories.models import Memory
from timeline.models import TimelineEvent
from notes.models import LoveNote
from goals.models import Goal
from countdowns.models import Countdown
from voice_messages.models import VoiceMessage


def landing_view(request):
    """Public landing page — redirects to dashboard if authenticated."""
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('dashboard:home')

    settings = CoupleSettings.get_settings()
    context = {
        'couple_settings': settings,
    }
    return render(request, 'landing.html', context)


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        today = timezone.now().date()
        couple_settings = CoupleSettings.get_settings()

        # Days together
        days_together = 0
        next_anniversary = None
        if couple_settings and couple_settings.relationship_start_date:
            start = couple_settings.relationship_start_date
            days_together = (today - start).days
            # Next anniversary
            try:
                anniversary_this_year = start.replace(year=today.year)
                if anniversary_this_year < today:
                    next_anniversary = start.replace(year=today.year + 1)
                else:
                    next_anniversary = anniversary_this_year
            except ValueError:
                next_anniversary = None

        # On This Day — memories from this month/day in previous years
        on_this_day = Memory.objects.filter(
            memory_date__month=today.month,
            memory_date__day=today.day,
        ).exclude(memory_date=today).order_by('-memory_date')[:3]

        # Recent memories
        recent_memories = Memory.objects.all().order_by('-memory_date')[:6]

        # Unread notes for current user
        unread_notes = LoveNote.objects.filter(
            receiver=request.user,
            is_delivered=True,
            is_archived=False,
        ).exclude(id__in=request.user.received_notes.filter(
            # A simple "read" check — we'll use a separate read tracking in a later iteration
        ).values('id') if False else []).order_by('-created_at')[:3]

        unread_notes_count = LoveNote.objects.filter(
            receiver=request.user,
            is_delivered=True,
            is_archived=False,
        ).count()

        # Active goals
        active_goals = Goal.objects.filter(completed=False).order_by('-created_at')[:3]

        # Upcoming countdowns
        upcoming_countdowns = Countdown.objects.filter(
            target_date__gte=today
        ).order_by('target_date')[:5]

        # Recent timeline events
        recent_timeline = TimelineEvent.objects.order_by('-event_date')[:4]

        # Quick stats
        memory_count = Memory.objects.count()
        note_count = LoveNote.objects.filter(is_delivered=True).count()
        voice_count = VoiceMessage.objects.count()
        timeline_count = TimelineEvent.objects.count()

        context = {
            'days_together': days_together,
            'next_anniversary': next_anniversary,
            'on_this_day': on_this_day,
            'recent_memories': recent_memories,
            'unread_notes': unread_notes,
            'unread_notes_count': unread_notes_count,
            'active_goals': active_goals,
            'upcoming_countdowns': upcoming_countdowns,
            'recent_timeline': recent_timeline,
            'memory_count': memory_count,
            'note_count': note_count,
            'voice_count': voice_count,
            'timeline_count': timeline_count,
            'couple_settings': couple_settings,
            'today': today,
        }
        return render(request, self.template_name, context)
