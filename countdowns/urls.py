from django.urls import path
from . import views

app_name = 'countdowns'

urlpatterns = [
    path('', views.CountdownListView.as_view(), name='list'),
    path('create/', views.CountdownCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.CountdownDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.CountdownUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.CountdownDeleteView.as_view(), name='delete'),
]
