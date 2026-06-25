"""goals/views.py — Goal tracker with contributions."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator

from .models import Goal, GoalContribution
from .forms import GoalForm, ContributionForm


@method_decorator(login_required, name='dispatch')
class GoalListView(View):
    template_name = 'goals/list.html'

    def get(self, request):
        active_goals = Goal.objects.filter(completed=False).order_by('-created_at')
        completed_goals = Goal.objects.filter(completed=True).order_by('-completed_at')
        return render(request, self.template_name, {
            'active_goals': active_goals,
            'completed_goals': completed_goals,
        })


@method_decorator(login_required, name='dispatch')
class GoalDetailView(View):
    template_name = 'goals/detail.html'

    def get(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        contributions = goal.contributions.order_by('-contributed_at')
        contribution_form = ContributionForm()
        return render(request, self.template_name, {
            'goal': goal,
            'contributions': contributions,
            'contribution_form': contribution_form,
        })


@method_decorator(login_required, name='dispatch')
class GoalCreateView(View):
    template_name = 'goals/form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': GoalForm(), 'title': 'New Goal'})

    def post(self, request):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save()
            messages.success(request, f'Goal "{goal.title}" created! 🎯')
            return redirect('goals:detail', pk=goal.pk)
        return render(request, self.template_name, {'form': form, 'title': 'New Goal'})


@method_decorator(login_required, name='dispatch')
class GoalUpdateView(View):
    template_name = 'goals/form.html'

    def get(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        return render(request, self.template_name, {'form': GoalForm(instance=goal), 'title': 'Edit Goal', 'goal': goal})

    def post(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated!')
            return redirect('goals:detail', pk=goal.pk)
        return render(request, self.template_name, {'form': form, 'title': 'Edit Goal', 'goal': goal})


@method_decorator(login_required, name='dispatch')
class GoalDeleteView(View):
    def post(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        goal.delete()
        messages.success(request, 'Goal removed.')
        return redirect('goals:list')


@method_decorator(login_required, name='dispatch')
class AddContributionView(View):
    def post(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.goal = goal
            contribution.save()
            messages.success(request, f'Added ${contribution.amount:.2f} to "{goal.title}"! 💰')
        else:
            messages.error(request, 'Invalid contribution. Please check the amount.')
        return redirect('goals:detail', pk=pk)
