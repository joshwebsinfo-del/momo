"""playlists/forms.py"""
from django import forms
from .models import Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'artist', 'youtube_url', 'memory_description')
        widgets = {
            'youtube_url': forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'memory_description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Why does this song matter to your relationship?',
            }),
        }

    def clean_youtube_url(self):
        url = self.cleaned_data.get('youtube_url', '')
        if 'youtube.com' not in url and 'youtu.be' not in url:
            raise forms.ValidationError('Please enter a valid YouTube URL.')
        return url
