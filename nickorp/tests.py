from django.contrib.auth.models import User
from django.test import TestCase


class AuthTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='user', password='user123'
        )

    def test_login_page_accessible(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_login(self):
        response = self.client.post('/login/', {
            'username': 'admin',
            'password': 'admin123',
        })
        self.assertRedirects(response, '/admin/', fetch_redirect_response=False)

    def test_regular_user_cannot_login(self):
        response = self.client.post('/login/', {
            'username': 'user',
            'password': 'user123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Accès réservé aux administrateurs')

    def test_invalid_credentials_rejected(self):
        response = self.client.post('/login/', {
            'username': 'admin',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Identifiants invalides')

    def test_logout_redirects_to_homepage(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post('/logout/')
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_homepage_has_no_login_link(self):
        response = self.client.get('/')
        self.assertNotContains(response, '/login/')
