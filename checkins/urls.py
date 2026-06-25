from django.urls import path

from .views import DailyCheckInCreateView, DailyCheckInListView

app_name = 'checkins'

urlpatterns = [
    path('', DailyCheckInListView.as_view(), name='list'),
    path('new/', DailyCheckInCreateView.as_view(), name='create'),
]
