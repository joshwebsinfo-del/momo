"""
accounts/forms.py — Registration, login, and profile forms.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.conf import settings

from .models import User, CoupleSettings


class CoupleRegistrationForm(UserCreationForm):
    """
    Registration form that enforces the Couple Access System.
    Only the two pre-approved email addresses may register.
    """
    first_name = forms.CharField(max_length=50, required=True, label='First Name')
    last_name = forms.CharField(max_length=50, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()

        # Check against DB settings first, fallback to env vars
        couple_settings = CoupleSettings.get_settings()
        if couple_settings:
            allowed = couple_settings.allowed_emails
        else:
            allowed = [e.lower() for e in settings.ALLOWED_COUPLE_EMAILS if e]

        if email not in allowed:
            raise forms.ValidationError(
                'This space is reserved for the owners of this Love Journey. '
                'If you believe this is an error, please contact the admin.'
            )

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    """Login form using email instead of username."""
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'autofocus': True, 'placeholder': 'your@email.com'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = '••••••••'


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile details."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell your story…'}),
        }


class ProfilePictureForm(forms.Form):
    """Form for uploading a new profile picture."""
    picture = forms.ImageField(
        label='Profile Picture',
        help_text='Max 10MB. JPG, PNG, or WebP.'
    )

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture:
            if picture.size > settings.MAX_IMAGE_SIZE:
                raise forms.ValidationError('Image must be smaller than 10 MB.')
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']
            if picture.content_type not in allowed_types:
                raise forms.ValidationError('Only JPG, PNG, or WebP images are allowed.')
        return picture
