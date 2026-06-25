from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import LoveNoteForm
from .models import LoveNote


class LoveNoteListView(LoginRequiredMixin, ListView):
    model = LoveNote
    template_name = 'notes/list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        qs = LoveNote.objects.filter(receiver=self.request.user).order_by('-created_at')
        for note in qs:
            if note.scheduled_for and note.scheduled_for <= date.today() and not note.is_delivered:
                note.is_delivered = True
                note.save(update_fields=['is_delivered'])
        return qs


class LoveNoteCreateView(LoginRequiredMixin, CreateView):
    model = LoveNote
    form_class = LoveNoteForm
    template_name = 'notes/form.html'
    success_url = reverse_lazy('notes:list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
