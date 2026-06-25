from django.urls import path

from .views import TimelineEventCreateView, TimelineEventDeleteView, TimelineEventListView, TimelineEventUpdateView

app_name = 'timeline'

urlpatterns = [
    path('', TimelineEventListView.as_view(), name='list'),
    path('new/', TimelineEventCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', TimelineEventUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', TimelineEventDeleteView.as_view(), name='delete'),
]
