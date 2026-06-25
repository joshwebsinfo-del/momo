"""api/serializers.py — DRF serializers for all models."""
from rest_framework import serializers
from memories.models import Memory
from timeline.models import TimelineEvent
from notes.models import LoveNote
from goals.models import Goal, GoalContribution
from countdowns.models import Countdown
from voice_messages.models import VoiceMessage
from playlists.models import Song
from notifications.models import Notification
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'display_name',
                  'profile_picture_url', 'bio', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class MemorySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.display_name', read_only=True)
    media_type = serializers.CharField(read_only=True)

    class Meta:
        model = Memory
        fields = ('id', 'title', 'description', 'photo_url', 'video_url',
                  'category', 'memory_date', 'location', 'created_by',
                  'created_by_name', 'media_type', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')


class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = ('id', 'title', 'description', 'image_url', 'event_date',
                  'event_icon', 'created_at')
        read_only_fields = ('id', 'created_at')


class LoveNoteSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.display_name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.display_name', read_only=True)

    class Meta:
        model = LoveNote
        fields = ('id', 'sender', 'sender_name', 'receiver', 'receiver_name',
                  'title', 'message', 'scheduled_for', 'is_delivered',
                  'is_favorite', 'is_archived', 'created_at')
        read_only_fields = ('id', 'sender', 'receiver', 'is_delivered', 'created_at')


class GoalContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalContribution
        fields = ('id', 'amount', 'note', 'contributed_at', 'created_at')
        read_only_fields = ('id', 'created_at')


class GoalSerializer(serializers.ModelSerializer):
    progress_percent = serializers.IntegerField(read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    contributions = GoalContributionSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = ('id', 'title', 'description', 'goal_type', 'target_amount',
                  'current_amount', 'target_date', 'completed', 'completed_at',
                  'progress_percent', 'remaining_amount', 'contributions',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'current_amount', 'completed', 'completed_at',
                            'created_at', 'updated_at')


class CountdownSerializer(serializers.ModelSerializer):
    days_remaining = serializers.IntegerField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    is_today = serializers.BooleanField(read_only=True)

    class Meta:
        model = Countdown
        fields = ('id', 'title', 'description', 'target_date', 'countdown_type',
                  'cover_emoji', 'is_recurring_yearly', 'days_remaining',
                  'is_past', 'is_today', 'created_at')
        read_only_fields = ('id', 'created_at')


class VoiceMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.display_name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.display_name', read_only=True)
    duration_display = serializers.CharField(read_only=True)

    class Meta:
        model = VoiceMessage
        fields = ('id', 'sender', 'sender_name', 'receiver', 'receiver_name',
                  'title', 'audio_url', 'duration_seconds', 'duration_display',
                  'is_listened', 'created_at')
        read_only_fields = ('id', 'sender', 'receiver', 'created_at')


class SongSerializer(serializers.ModelSerializer):
    added_by_name = serializers.CharField(source='added_by.display_name', read_only=True)
    youtube_embed_url = serializers.URLField(read_only=True)
    youtube_thumbnail = serializers.URLField(read_only=True)

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'youtube_url', 'youtube_embed_url',
                  'youtube_thumbnail', 'memory_description', 'added_by',
                  'added_by_name', 'created_at')
        read_only_fields = ('id', 'added_by', 'created_at')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'message', 'notification_type', 'link',
                  'is_read', 'created_at')
        read_only_fields = ('id', 'created_at')
