from django.urls import reverse
from django.contrib.auth.models import User

from users.tests.integration.test_login import AuthTestCase


class RegisterTest(AuthTestCase):
    def register(self, username, password):
        data = {
            'username': username,
            'password1': password,
            'password2': password,
        }
        response = self.client.post(reverse('users:register'), data=data)
        return response

    def test_register(self):
        self.assertRedirects(self.register(self.USERNAME, self.PASSWORD), 
                             reverse('rates'))

    def test_get_register_page(self):
        self.client.cookies.clear()
        response = self.client.get(reverse('users:register'))
        self.assertContains(response, 'input', count=4)

    def tearDown(self):
        User.objects.all().delete()

