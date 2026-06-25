"""playlists/urls.py"""
from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    path('', views.PlaylistView.as_view(), name='playlist'),
    path('add/', views.AddSongView.as_view(), name='add'),
    path('<uuid:pk>/edit/', views.EditSongView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.DeleteSongView.as_view(), name='delete'),
]
