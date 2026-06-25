from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CountdownViewSet, GoalViewSet, LoveNoteViewSet, MemoryViewSet, PlaylistViewSet, TimelineEventViewSet, VoiceMessageViewSet

router = DefaultRouter()
router.register(r'memories', MemoryViewSet)
router.register(r'timeline', TimelineEventViewSet)
router.register(r'notes', LoveNoteViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'countdowns', CountdownViewSet)
router.register(r'voice', VoiceMessageViewSet)
router.register(r'playlists', PlaylistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
