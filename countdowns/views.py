"""countdowns/views.py"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View, DetailView
from django.utils.decorators import method_decorator
from django.utils import timezone

from .models import Countdown
from .forms import CountdownForm


@method_decorator(login_required, name='dispatch')
class CountdownListView(View):
    template_name = 'countdowns/list.html'

    def get(self, request):
        today = timezone.now().date()
        upcoming = Countdown.objects.filter(target_date__gte=today).order_by('target_date')
        past = Countdown.objects.filter(target_date__lt=today).order_by('-target_date')
        return render(request, self.template_name, {
            'upcoming': upcoming,
            'past': past,
        })


@method_decorator(login_required, name='dispatch')
class CountdownCreateView(View):
    template_name = 'countdowns/form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': CountdownForm(), 'title': 'New Countdown'})

    def post(self, request):
        form = CountdownForm(request.POST)
        if form.is_valid():
            countdown = form.save()
            messages.success(request, f'Countdown to "{countdown.title}" created! ⏳')
            return redirect('countdowns:list')
        return render(request, self.template_name, {'form': form, 'title': 'New Countdown'})


@method_decorator(login_required, name='dispatch')
class CountdownUpdateView(View):
    template_name = 'countdowns/form.html'

    def get(self, request, pk):
        countdown = get_object_or_404(Countdown, pk=pk)
        return render(request, self.template_name, {
            'form': CountdownForm(instance=countdown),
            'title': 'Edit Countdown',
            'countdown': countdown,
        })

    def post(self, request, pk):
        countdown = get_object_or_404(Countdown, pk=pk)
        form = CountdownForm(request.POST, instance=countdown)
        if form.is_valid():
            form.save()
            messages.success(request, 'Countdown updated!')
            return redirect('countdowns:list')
        return render(request, self.template_name, {
            'form': form,
            'title': 'Edit Countdown',
            'countdown': countdown,
        })


@method_decorator(login_required, name='dispatch')
class CountdownDeleteView(View):
    def post(self, request, pk):
        countdown = get_object_or_404(Countdown, pk=pk)
        countdown.delete()
        messages.success(request, 'Countdown removed.')
        return redirect('countdowns:list')

class CountdownDetailView(DetailView):
    model = Countdown
    template_name = 'countdowns/detail.html'
    context_object_name = 'countdown'
