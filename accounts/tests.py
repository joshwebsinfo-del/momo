from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegistrationFlowTests(TestCase):
    def test_anyone_can_register_with_valid_details(self):
        response = self.client.post(
            reverse('accounts:register'),
            {
                'email': 'newuser@example.com',
                'username': 'newuser',
                'first_name': 'New',
                'last_name': 'User',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(email='newuser@example.com').exists())

    def test_duplicate_email_is_rejected(self):
        get_user_model().objects.create_user(
            email='taken@example.com',
            username='taken',
            first_name='Taken',
            last_name='User',
            password='StrongPass123!',
        )

        response = self.client.post(
            reverse('accounts:register'),
            {
                'email': 'taken@example.com',
                'username': 'another',
                'first_name': 'Another',
                'last_name': 'User',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertContains(response, 'already used')
        self.assertEqual(get_user_model().objects.filter(email='taken@example.com').count(), 1)
