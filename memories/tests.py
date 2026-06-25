from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from memories.models import Memory


class MemoryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='owner@example.com',
            username='owner',
            password='StrongPass123!',
            first_name='Love',
            last_name='Journey',
        )
        self.client.force_login(self.user)

    def test_memory_can_be_created(self):
        response = self.client.post(
            reverse('memories:create'),
            {
                'title': 'First Date',
                'description': 'A cherished evening',
                'category': 'Date',
                'memory_date': '2024-06-10',
                'location': 'Lakeview',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Memory.objects.filter(title='First Date').exists())
