from django import forms

from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('title', 'description', 'goal_type', 'target_amount', 'current_amount', 'target_date', 'completed')
