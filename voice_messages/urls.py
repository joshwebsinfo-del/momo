from django.urls import path
from . import views

app_name = 'voice_messages'

urlpatterns = [
    path('', views.VoiceMessageListView.as_view(), name='list'),
    path('record/', views.RecordView.as_view(), name='record'),
    path('upload/', views.UploadBlobView.as_view(), name='upload'),
    path('<uuid:pk>/delete/', views.DeleteVoiceMessageView.as_view(), name='delete'),
]
