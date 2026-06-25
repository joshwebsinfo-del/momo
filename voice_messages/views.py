from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .forms import VoiceMessageForm
from .models import VoiceMessage


class VoiceMessageListView(LoginRequiredMixin, ListView):
    model = VoiceMessage
    template_name = 'voice_messages/list.html'
    context_object_name = 'voice_messages'

    def get_queryset(self):
        return VoiceMessage.objects.filter(receiver=self.request.user).order_by('-created_at')


class VoiceMessageCreateView(LoginRequiredMixin, CreateView):
    model = VoiceMessage
    form_class = VoiceMessageForm
    template_name = 'voice_messages/form.html'
    success_url = reverse_lazy('voice_messages:list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


class VoiceMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = VoiceMessage
    template_name = 'voice_messages/confirm_delete.html'
    success_url = reverse_lazy('voice_messages:list')
