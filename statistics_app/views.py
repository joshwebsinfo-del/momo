"""statistics_app/views.py — Relationship statistics dashboard."""
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth

from memories.models import Memory
from notes.models import LoveNote
from voice_messages.models import VoiceMessage
from timeline.models import TimelineEvent
from goals.models import Goal
from countdowns.models import Countdown
from accounts.models import CoupleSettings


@method_decorator(login_required, name='dispatch')
class StatisticsView(View):
    template_name = 'statistics/statistics.html'

    def get(self, request):
        today = timezone.now().date()
        couple_settings = CoupleSettings.get_settings()

        # Core counts
        memory_count = Memory.objects.count()
        photo_count = Memory.objects.exclude(photo_url='').count()
        video_count = Memory.objects.exclude(video_url='').count()
        note_count = LoveNote.objects.filter(is_delivered=True).count()
        voice_count = VoiceMessage.objects.count()
        timeline_count = TimelineEvent.objects.count()
        goals_completed = Goal.objects.filter(completed=True).count()
        goals_active = Goal.objects.filter(completed=False).count()

        # Days together
        days_together = 0
        if couple_settings and couple_settings.relationship_start_date:
            days_together = (today - couple_settings.relationship_start_date).days

        # Memories by category (for pie/doughnut chart)
        memories_by_category = list(
            Memory.objects.values('category')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        category_labels = [m['category'].title() for m in memories_by_category]
        category_data = [m['count'] for m in memories_by_category]

        # Memories by month (last 12 months, for bar chart)
        twelve_months_ago = today.replace(day=1)
        monthly_memories = list(
            Memory.objects.filter(memory_date__gte=twelve_months_ago)
            .annotate(month=TruncMonth('memory_date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        monthly_labels = [m['month'].strftime('%b %Y') for m in monthly_memories]
        monthly_data = [m['count'] for m in monthly_memories]

        # Notes by month
        monthly_notes = list(
            LoveNote.objects.filter(is_delivered=True, created_at__date__gte=twelve_months_ago)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        notes_monthly_labels = [n['month'].strftime('%b %Y') for n in monthly_notes]
        notes_monthly_data = [n['count'] for n in monthly_notes]

        context = {
            'memory_count': memory_count,
            'photo_count': photo_count,
            'video_count': video_count,
            'note_count': note_count,
            'voice_count': voice_count,
            'timeline_count': timeline_count,
            'goals_completed': goals_completed,
            'goals_active': goals_active,
            'days_together': days_together,
            'couple_settings': couple_settings,
            # JSON for Chart.js
            'category_labels_json': json.dumps(category_labels),
            'category_data_json': json.dumps(category_data),
            'monthly_labels_json': json.dumps(monthly_labels),
            'monthly_data_json': json.dumps(monthly_data),
            'notes_monthly_labels_json': json.dumps(notes_monthly_labels),
            'notes_monthly_data_json': json.dumps(notes_monthly_data),
        }
        return render(request, self.template_name, context)
