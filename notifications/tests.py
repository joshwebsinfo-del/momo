from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from notifications.context_processors import notifications_processor


class NotificationsContextProcessorTests(TestCase):
    def test_returns_zero_when_notification_query_fails(self):
        request = RequestFactory().get('/')
        request.user = SimpleNamespace(is_authenticated=True)

        with patch('notifications.context_processors.Notification.objects.filter', side_effect=Exception('db down')):
            context = notifications_processor(request)

        self.assertEqual(context['unread_notifications_count'], 0)
