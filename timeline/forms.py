"""timeline/forms.py"""
from django import forms
from .models import TimelineEvent


class TimelineEventForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Event Photo')

    class Meta:
        model = TimelineEvent
        fields = ('title', 'description', 'event_date', 'event_icon')
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'event_icon': forms.TextInput(attrs={'placeholder': '❤️'}),
        }
