from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import MemoryCommentForm, MemoryForm
from .models import Memory, MemoryComment


class MemoryListView(LoginRequiredMixin, ListView):
    model = Memory
    template_name = 'memories/list.html'
    context_object_name = 'memories'

    def get_queryset(self):
        qs = Memory.objects.order_by('-memory_date')
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        year = self.request.GET.get('year')
        if query:
            qs = qs.filter(title__icontains=query)
        if category:
            qs = qs.filter(category=category)
        if year:
            qs = qs.filter(memory_date__year=year)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [choice[0] for choice in Memory.CATEGORY_CHOICES]
        context['years'] = sorted({memory.memory_date.year for memory in Memory.objects.all()}, reverse=True)
        return context


class MemoryCreateView(LoginRequiredMixin, CreateView):
    model = Memory
    form_class = MemoryForm
    template_name = 'memories/form.html'
    success_url = reverse_lazy('memories:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MemoryDetailView(LoginRequiredMixin, DetailView):
    model = Memory
    template_name = 'memories/detail.html'
    context_object_name = 'memory'

    def post(self, request, *args, **kwargs):
        memory = self.get_object()
        form = MemoryCommentForm(request.POST)
        if form.is_valid():
            MemoryComment.objects.create(memory=memory, author=request.user, message=form.cleaned_data['message'])
        return redirect('memories:detail', pk=memory.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        context['comment_form'] = MemoryCommentForm()
        return context


class MemoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Memory
    form_class = MemoryForm
    template_name = 'memories/form.html'
    success_url = reverse_lazy('memories:list')


class MemoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Memory
    template_name = 'memories/confirm_delete.html'
    success_url = reverse_lazy('memories:list')
