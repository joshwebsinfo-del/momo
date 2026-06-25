from django.urls import path

from .views import LoveNoteCreateView, LoveNoteListView

app_name = 'notes'

urlpatterns = [
    path('', LoveNoteListView.as_view(), name='list'),
    path('new/', LoveNoteCreateView.as_view(), name='create'),
]
