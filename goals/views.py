from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import GoalForm
from .models import Goal



class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'goals/list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.order_by('-updated_at')


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/form.html'
    success_url = reverse_lazy('goals:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.create_goal_reminder()
        return response


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/form.html'
    success_url = reverse_lazy('goals:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.create_goal_reminder()
        return response
