"""goals/forms.py"""
from django import forms
from .models import Goal, GoalContribution


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('title', 'description', 'goal_type', 'target_amount', 'target_date')
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's this goal about?"}),
            'target_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
        }


class ContributionForm(forms.ModelForm):
    class Meta:
        model = GoalContribution
        fields = ('amount', 'note', 'contributed_at')
        widgets = {
            'contributed_at': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01', 'placeholder': '0.00'}),
            'note': forms.TextInput(attrs={'placeholder': 'What was this for? (optional)'}),
        }
