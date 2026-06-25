from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DailyCheckInTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='checkin@example.com',
            username='checkin',
            first_name='Check',
            last_name='In',
            password='StrongPass123!',
        )

    def test_authenticated_user_can_create_checkin(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('checkins:create'),
            {
                'check_in_date': '2026-06-24',
                'mood': 'happy',
                'note': 'Lovely day together',
                'gratitude': 'Coffee and laughter',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.checkins.count(), 1)
