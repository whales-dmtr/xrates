from django.urls import reverse

from users.tests.integration.test_login import AuthTestCase


class LogoutTest(AuthTestCase):
    def setUp(self):
        register_data = {
            'username': self.USERNAME,
            'password1': self.PASSWORD,
            'password2': self.PASSWORD,
        }
        login_data = {
            'username': self.USERNAME,
            'password': self.PASSWORD,
        }
        self.client.post(reverse('users:register'), data=register_data)
        self.client.post(reverse('users:login'), data=login_data)

    def logout(self):
        return self.client.post(reverse('users:logout'))

    def test_logout(self):
        response = self.logout()
        self.assertTrue('sessionid=""' in \
                        str(response.cookies.get('sessionid')))

    def test_unauthorized_logout(self):
        self.client.cookies.clear()
        self.assertRedirects(
            self.client.post(reverse('users:logout')),
            reverse('users:login') + '?next=/users/logout'
        )