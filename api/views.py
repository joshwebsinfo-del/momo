from rest_framework import viewsets

from countdowns.models import Countdown
from goals.models import Goal
from memories.models import Memory
from notes.models import LoveNote
from playlists.models import Playlist
from timeline.models import TimelineEvent
from voice_messages.models import VoiceMessage

from .serializers import CountdownSerializer, GoalSerializer, LoveNoteSerializer, MemorySerializer, PlaylistSerializer, TimelineEventSerializer, VoiceMessageSerializer


class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer


class TimelineEventViewSet(viewsets.ModelViewSet):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer


class LoveNoteViewSet(viewsets.ModelViewSet):
    queryset = LoveNote.objects.all()
    serializer_class = LoveNoteSerializer


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class CountdownViewSet(viewsets.ModelViewSet):
    queryset = Countdown.objects.all()
    serializer_class = CountdownSerializer


class VoiceMessageViewSet(viewsets.ModelViewSet):
    queryset = VoiceMessage.objects.all()
    serializer_class = VoiceMessageSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
