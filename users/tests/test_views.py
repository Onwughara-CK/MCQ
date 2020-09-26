from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..forms import RegisterForm


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.response = cls.client.get('/')

    def test_url_resolves_to_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_correct_template(self):
        self.assertTemplateUsed(self.response, 'users/index.html')


class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.response = cls.client.get('/register/')

    def test_url_resolves_to_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_correct_template(self):
        self.assertTemplateUsed(self.response, 'users/register.html')

    def test_context_object(self):
        self.assertIn('title', self.response.context)
        self.assertIn('form', self.response.context)
        self.assertIsInstance(self.response.context.get('form'),RegisterForm)
        self.assertEqual('Register', self.response.context.get('title'))

    # POST
    def test_invalid_data(self):
        response = self.client.post('/register/', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_valid_data(self):
        response = self.client.post('/register/', {
            'email': 'jamesbond@test.com',
            'password1': '1234asdf7890',
            'password2': '1234asdf7890',
        })
        user = get_user_model().objects.get(email='jamesbond@test.com')
        self.assertEqual(user.email, 'jamesbond@test.com')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:home'))


class LoginViewTest(TestCase):
    """
    Test Login View
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.response = cls.client.get(reverse('users:login'))

        # create User instance
        cls.user = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

    def test_url_resolves_with_correct_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_correct_template(self):
        self.assertTemplateUsed(self.response, 'users/login.html')

    def test_user_is_redirect_if_authenticated(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 302)


class LogoutViewTest(TestCase):
    """
    Test Logout View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # create User instance
        cls.user = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

    def test_url_resolves_with_correct_status_code(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
