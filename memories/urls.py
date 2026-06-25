from django.urls import path
from . import views

app_name = 'memories'

urlpatterns = [
    path('', views.MemoryListView.as_view(), name='list'),
    path('add/', views.MemoryCreateView.as_view(), name='add'),
    path('<uuid:pk>/', views.MemoryDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.MemoryUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.MemoryDeleteView.as_view(), name='delete'),
]
