from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TimelineEventForm
from .models import TimelineEvent


class TimelineEventListView(LoginRequiredMixin, ListView):
    model = TimelineEvent
    template_name = 'timeline/list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return TimelineEvent.objects.order_by('event_date')


class TimelineEventCreateView(LoginRequiredMixin, CreateView):
    model = TimelineEvent
    form_class = TimelineEventForm
    template_name = 'timeline/form.html'
    success_url = reverse_lazy('timeline:list')


class TimelineEventUpdateView(LoginRequiredMixin, UpdateView):
    model = TimelineEvent
    form_class = TimelineEventForm
    template_name = 'timeline/form.html'
    success_url = reverse_lazy('timeline:list')


class TimelineEventDeleteView(LoginRequiredMixin, DeleteView):
    model = TimelineEvent
    template_name = 'timeline/confirm_delete.html'
    success_url = reverse_lazy('timeline:list')
