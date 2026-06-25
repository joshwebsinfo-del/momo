from django.urls import path

from .views import PrivateMessageCreateView, PrivateMessageListView

app_name = 'messages'

urlpatterns = [
    path('', PrivateMessageListView.as_view(), name='list'),
    path('new/', PrivateMessageCreateView.as_view(), name='create'),
]
