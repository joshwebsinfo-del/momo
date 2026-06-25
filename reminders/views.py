from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import ReminderForm
from .models import Reminder


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'reminders/list.html'
    context_object_name = 'reminders'

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user).order_by('reminder_date', 'title')


class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = ReminderForm
    template_name = 'reminders/form.html'
    success_url = reverse_lazy('reminders:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReminderUpdateView(LoginRequiredMixin, UpdateView):
    model = Reminder
    form_class = ReminderForm
    template_name = 'reminders/form.html'
    success_url = reverse_lazy('reminders:list')
