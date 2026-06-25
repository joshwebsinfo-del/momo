from django import forms

from .models import Countdown


class CountdownForm(forms.ModelForm):
    class Meta:
        model = Countdown
        fields = ('title', 'target_date', 'description')
