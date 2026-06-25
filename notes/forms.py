"""notes/forms.py"""
from django import forms
from .models import LoveNote


class LoveNoteForm(forms.ModelForm):
    scheduled_for = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Schedule for later (optional)',
        help_text='Leave blank to send immediately.',
    )

    class Meta:
        model = LoveNote
        fields = ('title', 'message', 'scheduled_for')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Give your note a title...'}),
            'message': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Write from your heart... ❤️',
                'class': 'love-note-textarea',
            }),
        }

    def __init__(self, *args, sender=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = sender
