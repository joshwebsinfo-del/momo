from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import CountdownForm
from .models import Countdown


class CountdownListView(LoginRequiredMixin, ListView):
    model = Countdown
    template_name = 'countdowns/list.html'
    context_object_name = 'countdowns'

    def get_queryset(self):
        return Countdown.objects.order_by('target_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context


class CountdownCreateView(LoginRequiredMixin, CreateView):
    model = Countdown
    form_class = CountdownForm
    template_name = 'countdowns/form.html'
    success_url = reverse_lazy('countdowns:list')


class CountdownUpdateView(LoginRequiredMixin, UpdateView):
    model = Countdown
    form_class = CountdownForm
    template_name = 'countdowns/form.html'
    success_url = reverse_lazy('countdowns:list')
