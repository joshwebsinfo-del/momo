"""voice_messages/views.py — Browser recording + file upload."""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from .models import VoiceMessage
from core.storage import upload_voice_message, upload_voice_blob

User = get_user_model()


def _get_partner(user):
    return User.objects.exclude(pk=user.pk).first()


@method_decorator(login_required, name='dispatch')
class VoiceMessageListView(View):
    template_name = 'voice_messages/list.html'

    def get(self, request):
        tab = request.GET.get('tab', 'inbox')
        if tab == 'sent':
            voice_msgs = VoiceMessage.objects.filter(sender=request.user).order_by('-created_at')
        else:
            voice_msgs = VoiceMessage.objects.filter(receiver=request.user).order_by('-created_at')
        return render(request, self.template_name, {'voice_msgs': voice_msgs, 'tab': tab})


@method_decorator(login_required, name='dispatch')
class RecordView(View):
    """Page with browser MediaRecorder UI + upload form fallback."""
    template_name = 'voice_messages/record.html'

    def get(self, request):
        partner = _get_partner(request.user)
        return render(request, self.template_name, {'partner': partner})


@method_decorator(login_required, name='dispatch')
class UploadBlobView(View):
    """AJAX endpoint: receives raw audio blob from browser MediaRecorder."""

    def post(self, request):
        try:
            audio_data = request.FILES.get('audio')
            title = request.POST.get('title', 'Voice Message')
            duration = int(request.POST.get('duration', 0))

            if not audio_data:
                return JsonResponse({'error': 'No audio data received.'}, status=400)

            partner = _get_partner(request.user)
            if not partner:
                return JsonResponse({'error': 'No partner found.'}, status=400)

            audio_url = upload_voice_message(audio_data, str(request.user.id))

            vm = VoiceMessage.objects.create(
                sender=request.user,
                receiver=partner,
                title=title or 'Voice Message',
                audio_url=audio_url,
                duration_seconds=duration,
            )

            # Notify partner
            from notifications.models import Notification
            Notification.objects.create(
                user=partner,
                title='🎙️ New Voice Message',
                message=f'{request.user.display_name} sent you a voice message!',
                notification_type='voice',
                link='/voice-messages/',
            )

            return JsonResponse({'success': True, 'id': str(vm.id)})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Upload failed. Please try again.'}, status=500)


@method_decorator(login_required, name='dispatch')
class DeleteVoiceMessageView(View):
    def post(self, request, pk):
        vm = get_object_or_404(VoiceMessage, pk=pk, sender=request.user)
        vm.delete()
        messages.success(request, 'Voice message deleted.')
        return redirect('voice_messages:list')
