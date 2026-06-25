from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import PlaylistForm
from .models import Playlist


class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'playlists/list.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        return Playlist.objects.order_by('-created_at')


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'playlists/form.html'
    success_url = reverse_lazy('playlists:list')
