"""statistics_app/urls.py"""
from django.urls import path
from . import views

app_name = 'statistics_app'

urlpatterns = [
    path('', views.StatisticsView.as_view(), name='statistics'),
]
