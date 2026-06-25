"""api/views.py — DRF ViewSets for all models."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q

from .permissions import IsCoupleUser
from .serializers import (
    UserSerializer, MemorySerializer, TimelineEventSerializer,
    LoveNoteSerializer, GoalSerializer, GoalContributionSerializer,
    CountdownSerializer, VoiceMessageSerializer, SongSerializer,
    NotificationSerializer,
)
from memories.models import Memory
from timeline.models import TimelineEvent
from notes.models import LoveNote
from goals.models import Goal, GoalContribution
from countdowns.models import Countdown
from voice_messages.models import VoiceMessage
from playlists.models import Song
from notifications.models import Notification

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only user info for the couple."""
    permission_classes = [IsCoupleUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Return the currently authenticated user's profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class MemoryViewSet(viewsets.ModelViewSet):
    """Full CRUD for memories."""
    permission_classes = [IsCoupleUser]
    serializer_class = MemorySerializer
    queryset = Memory.objects.all().order_by('-memory_date')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        year = self.request.query_params.get('year')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category=category)
        if year:
            qs = qs.filter(memory_date__year=year)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        return qs


class TimelineEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCoupleUser]
    serializer_class = TimelineEventSerializer
    queryset = TimelineEvent.objects.all().order_by('event_date')


class LoveNoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCoupleUser]
    serializer_class = LoveNoteSerializer

    def get_queryset(self):
        user = self.request.user
        return LoveNote.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        partner = User.objects.exclude(pk=self.request.user.pk).first()
        serializer.save(sender=self.request.user, receiver=partner)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        note = self.get_object()
        note.is_favorite = not note.is_favorite
        note.save(update_fields=['is_favorite'])
        return Response({'is_favorite': note.is_favorite})

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        note = self.get_object()
        note.is_archived = True
        note.save(update_fields=['is_archived'])
        return Response({'archived': True})


class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCoupleUser]
    serializer_class = GoalSerializer
    queryset = Goal.objects.all().order_by('-created_at')

    @action(detail=True, methods=['post'])
    def contribute(self, request, pk=None):
        goal = self.get_object()
        serializer = GoalContributionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(goal=goal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountdownViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCoupleUser]
    serializer_class = CountdownSerializer
    queryset = Countdown.objects.all().order_by('target_date')


class VoiceMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCoupleUser]
    serializer_class = VoiceMessageSerializer

    def get_queryset(self):
        user = self.request.user
        return VoiceMessage.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        partner = User.objects.exclude(pk=self.request.user.pk).first()
        serializer.save(sender=self.request.user, receiver=partner)


class SongViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCoupleUser]
    serializer_class = SongSerializer
    queryset = Song.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsCoupleUser]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.is_read = True
        notif.save(update_fields=['is_read'])
        return Response({'read': True})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'count': count})
