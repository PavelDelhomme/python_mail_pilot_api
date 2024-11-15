from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class IMAPSettingsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_configure_imap(self):
        data = {
            "imap_email": "test@delhomme.ovh",
            "imap_password": "securepassword",
            "imap_host": "imap.mail.ovh.net"
        }
        response = self.client.post('/api/configure_imap/', data)
        self.assertEqual(response.status_code, 200)

    def test_get_imap_settings(self):
        self.test_configure_imap()  # Configure first
        response = self.client.get('/api/get_imap_settings/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("imap_email", response.data)
