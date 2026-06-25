"""goals/urls.py"""
from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.GoalListView.as_view(), name='list'),
    path('create/', views.GoalCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.GoalDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.GoalUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.GoalDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/contribute/', views.AddContributionView.as_view(), name='contribute'),
]
