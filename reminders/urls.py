from django.urls import path

from .views import ReminderCreateView, ReminderListView, ReminderUpdateView

app_name = 'reminders'

urlpatterns = [
    path('', ReminderListView.as_view(), name='list'),
    path('new/', ReminderCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', ReminderUpdateView.as_view(), name='update'),
]
