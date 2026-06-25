"""playlists/views.py"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator

from .models import Song
from .forms import SongForm


@method_decorator(login_required, name='dispatch')
class PlaylistView(View):
    template_name = 'playlists/playlist.html'

    def get(self, request):
        songs = Song.objects.all().order_by('-created_at')
        return render(request, self.template_name, {'songs': songs})


@method_decorator(login_required, name='dispatch')
class AddSongView(View):
    template_name = 'playlists/form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': SongForm(), 'title': 'Add a Song'})

    def post(self, request):
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.added_by = request.user
            song.save()
            messages.success(request, f'"{song.title}" added to your playlist! 🎵')
            return redirect('playlists:playlist')
        return render(request, self.template_name, {'form': form, 'title': 'Add a Song'})


@method_decorator(login_required, name='dispatch')
class EditSongView(View):
    template_name = 'playlists/form.html'

    def get(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        return render(request, self.template_name, {'form': SongForm(instance=song), 'title': 'Edit Song', 'song': song})

    def post(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, 'Song updated!')
            return redirect('playlists:playlist')
        return render(request, self.template_name, {'form': form, 'title': 'Edit Song', 'song': song})


@method_decorator(login_required, name='dispatch')
class DeleteSongView(View):
    def post(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        song.delete()
        messages.success(request, 'Song removed from playlist.')
        return redirect('playlists:playlist')
