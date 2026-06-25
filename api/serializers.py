from rest_framework import serializers

from countdowns.models import Countdown
from goals.models import Goal
from memories.models import Memory
from notes.models import LoveNote
from playlists.models import Playlist
from timeline.models import TimelineEvent
from voice_messages.models import VoiceMessage


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'


class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = '__all__'


class LoveNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoveNote
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'


class CountdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countdown
        fields = '__all__'


class VoiceMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceMessage
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
