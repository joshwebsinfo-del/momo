from django import forms

from .models import Memory, MemoryComment


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ('title', 'description', 'photo', 'video', 'category', 'memory_date', 'location')


class MemoryCommentForm(forms.ModelForm):
    class Meta:
        model = MemoryComment
        fields = ('message',)
