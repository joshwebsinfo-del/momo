from django import forms

from .models import TimelineEvent


class TimelineEventForm(forms.ModelForm):
    class Meta:
        model = TimelineEvent
        fields = ('title', 'description', 'image', 'event_date')
