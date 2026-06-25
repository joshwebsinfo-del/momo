"""notes/views.py — Love Notes CRUD with future delivery."""
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from .models import LoveNote
from .forms import LoveNoteForm

User = get_user_model()


def _get_partner(user):
    """Return the other user (partner) in the couple."""
    return User.objects.exclude(pk=user.pk).first()


@method_decorator(login_required, name='dispatch')
class InboxView(View):
    template_name = 'notes/inbox.html'

    def get(self, request):
        notes = LoveNote.objects.filter(
            receiver=request.user,
            is_delivered=True,
            is_archived=False,
        ).order_by('-created_at')
        return render(request, self.template_name, {'notes': notes, 'view': 'inbox'})


@method_decorator(login_required, name='dispatch')
class SentView(View):
    template_name = 'notes/inbox.html'

    def get(self, request):
        notes = LoveNote.objects.filter(
            sender=request.user,
        ).order_by('-created_at')
        return render(request, self.template_name, {'notes': notes, 'view': 'sent'})


@method_decorator(login_required, name='dispatch')
class FavoritesView(View):
    template_name = 'notes/inbox.html'

    def get(self, request):
        notes = LoveNote.objects.filter(
            receiver=request.user,
            is_favorite=True,
            is_delivered=True,
        ).order_by('-created_at')
        return render(request, self.template_name, {'notes': notes, 'view': 'favorites'})


@method_decorator(login_required, name='dispatch')
class ScheduledView(View):
    template_name = 'notes/inbox.html'

    def get(self, request):
        notes = LoveNote.objects.filter(
            sender=request.user,
            is_delivered=False,
        ).order_by('scheduled_for')
        return render(request, self.template_name, {'notes': notes, 'view': 'scheduled'})


@method_decorator(login_required, name='dispatch')
class ComposeView(View):
    template_name = 'notes/compose.html'

    def get(self, request):
        partner = _get_partner(request.user)
        form = LoveNoteForm(sender=request.user)
        return render(request, self.template_name, {'form': form, 'partner': partner})

    def post(self, request):
        form = LoveNoteForm(request.POST, sender=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.sender = request.user
            note.receiver = _get_partner(request.user)
            note.save()
            if note.is_delivered:
                messages.success(request, f'Your note "{note.title}" has been delivered! 💌')
            else:
                messages.success(request, f'Your note is scheduled for {note.scheduled_for.strftime("%B %d, %Y")}! 📅')
            return redirect('notes:inbox')
        partner = _get_partner(request.user)
        return render(request, self.template_name, {'form': form, 'partner': partner})


@method_decorator(login_required, name='dispatch')
class NoteDetailView(View):
    template_name = 'notes/detail.html'

    def get(self, request, pk):
        note = get_object_or_404(
            LoveNote,
            pk=pk,
            is_delivered=True,
        )
        # Only sender or receiver may view
        if note.sender != request.user and note.receiver != request.user:
            messages.error(request, 'You do not have access to this note.')
            return redirect('notes:inbox')
        return render(request, self.template_name, {'note': note})


@method_decorator(login_required, name='dispatch')
class FavoriteToggleView(View):
    def post(self, request, pk):
        note = get_object_or_404(LoveNote, pk=pk, receiver=request.user)
        note.is_favorite = not note.is_favorite
        note.save(update_fields=['is_favorite'])
        return redirect('notes:detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class ArchiveView(View):
    def post(self, request, pk):
        note = get_object_or_404(LoveNote, pk=pk, receiver=request.user)
        note.is_archived = True
        note.save(update_fields=['is_archived'])
        messages.success(request, 'Note archived.')
        return redirect('notes:inbox')


@method_decorator(login_required, name='dispatch')
class DeleteNoteView(View):
    def post(self, request, pk):
        note = get_object_or_404(LoveNote, pk=pk, sender=request.user)
        note.delete()
        messages.success(request, 'Note deleted.')
        return redirect('notes:sent')

# -------------------------------------------------------------------
# Generic class‑based views for CRUD operations (used by urls.py)
# -------------------------------------------------------------------

class NoteListView(ListView):
    model = LoveNote
    template_name = 'notes/list.html'
    context_object_name = 'notes'
    paginate_by = 20
    def get_queryset(self):
        # Show notes owned by the user (sent or received) and delivered
        return LoveNote.objects.filter(
            models.Q(sender=self.request.user) | models.Q(receiver=self.request.user),
            is_delivered=True
        ).order_by('-created_at')

class NoteCreateView(CreateView):
    model = LoveNote
    form_class = LoveNoteForm
    template_name = 'notes/create.html'
    success_url = '/notes/'
    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = _get_partner(self.request.user)
        return super().form_valid(form)

class NoteUpdateView(UpdateView):
    model = LoveNote
    form_class = LoveNoteForm
    template_name = 'notes/update.html'
    success_url = '/notes/'
    def get_queryset(self):
        # Only allow sender to edit unsent notes
        return LoveNote.objects.filter(sender=self.request.user, is_delivered=False)

class NoteDeleteView(DeleteView):
    model = LoveNote
    template_name = 'notes/delete.html'
    success_url = '/notes/'
    def get_queryset(self):
        # Only sender can delete their notes
        return LoveNote.objects.filter(sender=self.request.user)

