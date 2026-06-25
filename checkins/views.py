from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import DailyCheckInForm
from .models import DailyCheckIn


class DailyCheckInListView(LoginRequiredMixin, ListView):
    model = DailyCheckIn
    template_name = 'checkins/list.html'
    context_object_name = 'checkins'

    def get_queryset(self):
        return DailyCheckIn.objects.filter(user=self.request.user).order_by('-check_in_date')


class DailyCheckInCreateView(LoginRequiredMixin, CreateView):
    model = DailyCheckIn
    form_class = DailyCheckInForm
    template_name = 'checkins/form.html'
    success_url = reverse_lazy('checkins:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
