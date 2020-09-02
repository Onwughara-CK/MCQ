from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTest(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_user_is_created(self):
        user = self.User.objects.create_user(
            email='test@gmail.com')
        self.assertEqual(str(user), 'test@gmail.com')
        self.assertTrue(user.is_active, True)
        self.assertFalse(user.is_staff, False)
        self.assertFalse(user.is_superuser, True)
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='')

    def test_superuser_is_created(self):
        user = self.User.objects.create_superuser(
            email='test@gmail.com', password='asdf7890')
        self.assertEqual(str(user), 'test@gmail.com')
        self.assertEqual(user.is_superuser, True)
