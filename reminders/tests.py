from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ReminderTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='reminder@example.com',
            username='reminder',
            first_name='Reminder',
            last_name='User',
            password='StrongPass123!',
        )

    def test_authenticated_user_can_create_reminder(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('reminders:create'),
            {
                'title': 'Anniversary',
                'reminder_date': '2026-07-14',
                'note': 'Plan a lovely dinner',
                'is_done': 'on',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.reminders.count(), 1)
