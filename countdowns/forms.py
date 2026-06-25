"""countdowns/forms.py"""
from django import forms
from .models import Countdown


class CountdownForm(forms.ModelForm):
    class Meta:
        model = Countdown
        fields = ('title', 'description', 'target_date', 'countdown_type', 'cover_emoji', 'is_recurring_yearly')
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'cover_emoji': forms.TextInput(attrs={'placeholder': '🎉', 'maxlength': '10'}),
        }
