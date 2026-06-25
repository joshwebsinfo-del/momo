from django import forms

from .models import PrivateMessage


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ('receiver', 'content')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
