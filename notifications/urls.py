"""notifications/urls.py"""
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),
    path('<uuid:pk>/read/', views.MarkReadView.as_view(), name='mark_read'),
    path('unread-count/', views.UnreadCountView.as_view(), name='unread_count'),
    path('clear/', views.ClearAllView.as_view(), name='clear_all'),
]
