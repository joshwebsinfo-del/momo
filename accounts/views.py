"""
accounts/views.py — Authentication and profile views.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import CoupleRegistrationForm, EmailAuthenticationForm, ProfileUpdateForm, ProfilePictureForm
from .models import User
from core.storage import upload_profile_picture


class RegisterView(View):
    """
    Registration view enforcing the Couple Access System.
    Only two pre-approved emails may create accounts.
    """
    template_name = 'accounts/register.html'

    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = CoupleRegistrationForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')

        form = CoupleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Welcome, {user.first_name}! Your Love Journey begins now. ❤️'
            )
            return redirect('dashboard:home')

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """Email-based login with rate limiting."""
    template_name = 'accounts/login.html'

    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = EmailAuthenticationForm(request)
        return render(request, self.template_name, {'form': form})

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')

        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'dashboard:home')
            messages.success(request, f'Welcome back, {user.display_name}! ❤️')
            return redirect(next_url)

        messages.error(request, 'Invalid email or password. Please try again.')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    """POST-only logout view."""
    def post(self, request):
        logout(request)
        messages.info(request, 'You have been signed out. See you soon! 💕')
        return redirect('landing')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """View and update user profile."""
    template_name = 'accounts/profile.html'

    def get(self, request):
        profile_form = ProfileUpdateForm(instance=request.user)
        picture_form = ProfilePictureForm()
        password_form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {
            'profile_form': profile_form,
            'picture_form': picture_form,
            'password_form': password_form,
        })

    def post(self, request):
        action = request.POST.get('action', 'profile')

        if action == 'profile':
            form = ProfileUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully! ✨')
                return redirect('accounts:profile')
            picture_form = ProfilePictureForm()
            password_form = PasswordChangeForm(user=request.user)
            return render(request, self.template_name, {
                'profile_form': form,
                'picture_form': picture_form,
                'password_form': password_form,
            })

        elif action == 'picture':
            form = ProfilePictureForm(request.POST, request.FILES)
            if form.is_valid():
                picture = form.cleaned_data['picture']
                try:
                    url = upload_profile_picture(picture, str(request.user.id))
                    request.user.profile_picture_url = url
                    request.user.save(update_fields=['profile_picture_url'])
                    messages.success(request, 'Profile picture updated! 📸')
                except Exception as e:
                    messages.error(request, f'Upload failed: {e}')
            else:
                messages.error(request, 'Invalid file. Please try again.')
            return redirect('accounts:profile')

        elif action == 'password':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully! 🔐')
                return redirect('accounts:profile')
            profile_form = ProfileUpdateForm(instance=request.user)
            picture_form = ProfilePictureForm()
            return render(request, self.template_name, {
                'profile_form': profile_form,
                'picture_form': picture_form,
                'password_form': form,
            })

        return redirect('accounts:profile')
