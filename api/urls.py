"""api/urls.py"""
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'memories', views.MemoryViewSet, basename='memory')
router.register(r'timeline', views.TimelineEventViewSet, basename='timeline')
router.register(r'notes', views.LoveNoteViewSet, basename='note')
router.register(r'goals', views.GoalViewSet, basename='goal')
router.register(r'countdowns', views.CountdownViewSet, basename='countdown')
router.register(r'voice-messages', views.VoiceMessageViewSet, basename='voicemessage')
router.register(r'songs', views.SongViewSet, basename='song')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
