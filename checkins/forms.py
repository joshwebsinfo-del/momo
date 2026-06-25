from django import forms

from .models import DailyCheckIn


class DailyCheckInForm(forms.ModelForm):
    class Meta:
        model = DailyCheckIn
        fields = ('check_in_date', 'mood', 'note', 'gratitude')
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
            'gratitude': forms.Textarea(attrs={'rows': 3}),
        }
