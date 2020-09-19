from django.test import SimpleTestCase
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import resolve, reverse

from ..views import IndexView, RegisterView


class UrlTest(SimpleTestCase):

    ### INDEX VIEW TEST ###
    def test_index_url_resolves_to_index_view(self):
        url = reverse('users:home')
        self.assertURLEqual(url, '/')
        self.assertEqual(resolve(url).func.view_class, IndexView)

    ### REGISTER VIEW TEST ###
    def test_register_url_resolves_to_register_view(self):
        url = reverse('users:register')
        self.assertURLEqual(url, '/register/')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    ### LOGIN VIEW TEST ###
    def test_login_url_resolves_to_login_view(self):
        url = reverse('users:login')
        self.assertURLEqual(url, '/login/')
        self.assertEqual(resolve(url).func.view_class, LoginView)

     ### LOGOUT VIEW TEST ###
    def test_logout_url_resolves_to_logout_view(self):
        url = reverse('users:logout')
        self.assertURLEqual(url, '/logout/')
        self.assertEqual(resolve(url).func.view_class, LogoutView)
