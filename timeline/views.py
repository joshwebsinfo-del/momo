"""timeline/views.py"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator

from .models import TimelineEvent
from .forms import TimelineEventForm
from core.storage import upload_timeline_image


@method_decorator(login_required, name='dispatch')
class TimelineView(View):
    template_name = 'timeline/timeline.html'

    def get(self, request):
        events = TimelineEvent.objects.all().order_by('event_date')
        return render(request, self.template_name, {'events': events})


@method_decorator(login_required, name='dispatch')
class EventCreateView(View):
    template_name = 'timeline/event_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': TimelineEventForm()})

    def post(self, request):
        form = TimelineEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            image = request.FILES.get('image')
            if image:
                try:
                    event.image_url = upload_timeline_image(image, str(request.user.id))
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, self.template_name, {'form': form})
            event.save()
            messages.success(request, f'"{event.title}" added to your timeline! 🌟')
            return redirect('timeline:timeline')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class EventUpdateView(View):
    template_name = 'timeline/event_form.html'

    def get(self, request, pk):
        event = get_object_or_404(TimelineEvent, pk=pk)
        return render(request, self.template_name, {'form': TimelineEventForm(instance=event), 'event': event})

    def post(self, request, pk):
        event = get_object_or_404(TimelineEvent, pk=pk)
        form = TimelineEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            image = request.FILES.get('image')
            if image:
                try:
                    event.image_url = upload_timeline_image(image, str(request.user.id))
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, self.template_name, {'form': form, 'event': event})
            event.save()
            messages.success(request, 'Timeline event updated!')
            return redirect('timeline:timeline')
        return render(request, self.template_name, {'form': form, 'event': event})


@method_decorator(login_required, name='dispatch')
class EventDeleteView(View):
    def post(self, request, pk):
        event = get_object_or_404(TimelineEvent, pk=pk)
        event.delete()
        messages.success(request, 'Event removed from timeline.')
        return redirect('timeline:timeline')
