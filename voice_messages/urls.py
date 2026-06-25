from django.urls import path

from .views import VoiceMessageCreateView, VoiceMessageDeleteView, VoiceMessageListView

app_name = 'voice_messages'

urlpatterns = [
    path('', VoiceMessageListView.as_view(), name='list'),
    path('new/', VoiceMessageCreateView.as_view(), name='create'),
    path('<uuid:pk>/delete/', VoiceMessageDeleteView.as_view(), name='delete'),
]
