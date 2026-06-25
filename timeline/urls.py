"""timeline/urls.py"""
from django.urls import path
from . import views

app_name = 'timeline'

urlpatterns = [
    path('', views.TimelineView.as_view(), name='timeline'),
    path('add/', views.EventCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.EventUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.EventDeleteView.as_view(), name='delete'),
]
