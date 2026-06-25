from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from dashboard.views import DashboardView


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='dashboard@example.com', username='dashboard', password='secret123')

    def test_dashboard_handles_database_errors_gracefully(self):
        request = RequestFactory().get('/dashboard/')
        request.user = self.user

        with patch('dashboard.views.Memory.objects.order_by', side_effect=Exception('db down')):
            response = DashboardView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your love dashboard')

    @override_settings(ROOT_URLCONF='config.urls', ALLOWED_HOSTS=['testserver'])
    def test_dashboard_template_renders_without_reverse_lookup_errors(self):
        self.client.force_login(self.user)
        response = self.client.get('/dashboard/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
