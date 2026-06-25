from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from goals.models import Goal
from reminders.models import Reminder


class GoalAutomationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='goal@example.com',
            username='goaluser',
            password='StrongPass123!',
            first_name='Goal',
            last_name='User',
        )
        self.client.force_login(self.user)

    def test_goal_creation_creates_a_deadline_reminder(self):
        response = self.client.post(
            reverse('goals:create'),
            {
                'title': 'Save for trip',
                'description': 'Plan a getaway',
                'target_amount': '1000.00',
                'current_amount': '200.00',
                'target_date': '2026-12-31',
                'goal_type': 'Travel',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Goal.objects.filter(title='Save for trip').exists())
        self.assertTrue(Reminder.objects.filter(title='Goal deadline: Save for trip').exists())
