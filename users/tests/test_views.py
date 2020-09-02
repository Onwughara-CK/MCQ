from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post(self):
        url = reverse('users:register')
        response = self.client.post(url, {
            'email': 'jamesbond@test.com',
            'password1': '1234asdf7890',
            'password2': '1234asdf7890',
        })
        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(email='jamesbond@test.com')
        self.assertEqual(str(user), 'jamesbond@test.com')
