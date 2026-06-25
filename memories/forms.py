"""memories/forms.py"""
from django import forms
from .models import Memory


class MemoryForm(forms.ModelForm):
    photo = forms.ImageField(required=False, label='Upload Photo')
    video = forms.FileField(required=False, label='Upload Video')

    class Meta:
        model = Memory
        fields = ('title', 'description', 'category', 'memory_date', 'location')
        widgets = {
            'memory_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe this memory...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where was this? (optional)'}),
        }
