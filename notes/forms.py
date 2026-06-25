from django import forms

from .models import LoveNote


class LoveNoteForm(forms.ModelForm):
    class Meta:
        model = LoveNote
        fields = ('receiver', 'title', 'message', 'scheduled_for', 'is_favorite', 'is_archived')
