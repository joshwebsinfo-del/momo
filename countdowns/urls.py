from django.urls import path

from .views import CountdownCreateView, CountdownListView, CountdownUpdateView

app_name = 'countdowns'

urlpatterns = [
    path('', CountdownListView.as_view(), name='list'),
    path('new/', CountdownCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', CountdownUpdateView.as_view(), name='update'),
]
