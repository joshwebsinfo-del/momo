from django.urls import path

from .views import PlaylistCreateView, PlaylistListView

app_name = 'playlists'

urlpatterns = [
    path('', PlaylistListView.as_view(), name='list'),
    path('new/', PlaylistCreateView.as_view(), name='create'),
]
