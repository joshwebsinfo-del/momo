from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from countdowns.models import Countdown
from goals.models import Goal
from memories.models import Memory
from notes.models import LoveNote
from timeline.models import TimelineEvent
from voice_messages.models import VoiceMessage


class StatsView(LoginRequiredMixin, TemplateView):
    template_name = 'stats/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'stats': {
                'days_together': (date.today() - self.request.user.created_at.date()).days,
                'memories': Memory.objects.count(),
                'photos': Memory.objects.exclude(photo='').count(),
                'videos': Memory.objects.exclude(video='').count(),
                'notes_sent': LoveNote.objects.count(),
                'voice_notes': VoiceMessage.objects.count(),
                'timeline_events': TimelineEvent.objects.count(),
                'goals_completed': Goal.objects.filter(completed=True).count(),
            },
            'countdowns': Countdown.objects.count(),
        })
        return context
