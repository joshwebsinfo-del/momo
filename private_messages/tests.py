from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PrivateMessageTests(TestCase):
    def setUp(self):
        self.sender = get_user_model().objects.create_user(
            email='sender@example.com',
            username='sender',
            first_name='Sender',
            last_name='User',
            password='StrongPass123!',
        )
        self.receiver = get_user_model().objects.create_user(
            email='receiver@example.com',
            username='receiver',
            first_name='Receiver',
            last_name='User',
            password='StrongPass123!',
        )

    def test_authenticated_user_can_send_message(self):
        self.client.force_login(self.sender)
        response = self.client.post(
            reverse('messages:create'),
            {
                'receiver': self.receiver.pk,
                'content': 'Hello love',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.sender.sent_messages.count(), 1)
