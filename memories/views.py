"""memories/views.py"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import Memory
from .forms import MemoryForm
from core.storage import upload_memory_photo, upload_memory_video


@method_decorator(login_required, name='dispatch')
class MemoryListView(View):
    template_name = 'memories/gallery.html'

    def get(self, request):
        memories = Memory.objects.all()

        # Filters
        category = request.GET.get('category', '')
        year = request.GET.get('year', '')
        search = request.GET.get('search', '')

        if category:
            memories = memories.filter(category=category)
        if year:
            memories = memories.filter(memory_date__year=year)
        if search:
            memories = memories.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )

        # Available years for filter
        years = Memory.objects.dates('memory_date', 'year', order='DESC')

        context = {
            'memories': memories,
            'categories': Memory.CATEGORY_CHOICES,
            'years': years,
            'selected_category': category,
            'selected_year': year,
            'search_query': search,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class MemoryDetailView(View):
    template_name = 'memories/detail.html'

    def get(self, request, pk):
        memory = get_object_or_404(Memory, pk=pk)
        return render(request, self.template_name, {'memory': memory})


@method_decorator(login_required, name='dispatch')
class MemoryCreateView(View):
    template_name = 'memories/create.html'

    def get(self, request):
        form = MemoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.created_by = request.user

            # Handle photo upload
            photo = request.FILES.get('photo')
            if photo:
                try:
                    memory.photo_url = upload_memory_photo(photo, str(request.user.id))
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, self.template_name, {'form': form})

            # Handle video upload
            video = request.FILES.get('video')
            if video:
                try:
                    memory.video_url = upload_memory_video(video, str(request.user.id))
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, self.template_name, {'form': form})

            memory.save()
            messages.success(request, f'Memory "{memory.title}" saved! 💕')
            return redirect('memories:detail', pk=memory.pk)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class MemoryUpdateView(View):
    template_name = 'memories/edit.html'

    def get(self, request, pk):
        memory = get_object_or_404(Memory, pk=pk)
        form = MemoryForm(instance=memory)
        return render(request, self.template_name, {'form': form, 'memory': memory})

    def post(self, request, pk):
        memory = get_object_or_404(Memory, pk=pk)
        form = MemoryForm(request.POST, request.FILES, instance=memory)
        if form.is_valid():
            memory = form.save(commit=False)

            photo = request.FILES.get('photo')
            if photo:
                try:
                    memory.photo_url = upload_memory_photo(photo, str(request.user.id))
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, self.template_name, {'form': form, 'memory': memory})

            video = request.FILES.get('video')
            if video:
                try:
                    memory.video_url = upload_memory_video(video, str(request.user.id))
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, self.template_name, {'form': form, 'memory': memory})

            memory.save()
            messages.success(request, 'Memory updated! ✨')
            return redirect('memories:detail', pk=memory.pk)

        return render(request, self.template_name, {'form': form, 'memory': memory})


@method_decorator(login_required, name='dispatch')
class MemoryDeleteView(View):
    def post(self, request, pk):
        memory = get_object_or_404(Memory, pk=pk)
        title = memory.title
        memory.delete()
        messages.success(request, f'"{title}" has been removed.')
        return redirect('memories:gallery')
