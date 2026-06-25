from django.urls import path

from .views import MemoryCreateView, MemoryDeleteView, MemoryDetailView, MemoryListView, MemoryUpdateView

app_name = 'memories'

urlpatterns = [
    path('', MemoryListView.as_view(), name='list'),
    path('new/', MemoryCreateView.as_view(), name='create'),
    path('<uuid:pk>/', MemoryDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', MemoryUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', MemoryDeleteView.as_view(), name='delete'),
]
