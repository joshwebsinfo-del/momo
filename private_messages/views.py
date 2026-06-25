from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import PrivateMessageForm
from .models import PrivateMessage


class PrivateMessageListView(LoginRequiredMixin, ListView):
    model = PrivateMessage
    template_name = 'messages/list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return PrivateMessage.objects.filter(receiver=self.request.user).order_by('-created_at')


class PrivateMessageCreateView(LoginRequiredMixin, CreateView):
    model = PrivateMessage
    form_class = PrivateMessageForm
    template_name = 'messages/form.html'
    success_url = reverse_lazy('messages:list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
