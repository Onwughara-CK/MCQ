from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up unmodifiable test data
        cls.user = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

    def test_teacher_label(self):
        field_label = self.user._meta.get_field('teacher').verbose_name
        self.assertEqual(field_label, 'teacher')

    def test_teacher_default(self):
        default = self.user._meta.get_field('teacher').default
        self.assertFalse(default)

    def test_email_label(self):
        field_label = self.user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_email_max_length(self):
        max_length = self.user._meta.get_field('email').max_length
        self.assertEqual(max_length, 255)

    def test_email_unique(self):
        unique = self.user._meta.get_field('email').unique
        self.assertTrue(unique)

    def test_username_is_none(self):
        self.assertIsNone(self.user.username)

    def test_username_field_is_email(self):
        self.assertEqual(self.user.USERNAME_FIELD, 'email')

    def test_required_fields_is_empty(self):
        self.assertEqual(self.user.REQUIRED_FIELDS, [])

    def test_username_is_email(self):
        self.assertEqual(self.user.get_username(), self.user.email)

    def test_str(self):
        self.assertEqual(str(self.user), self.user.email)


class CustomUserManagerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up unmodifiable test data
        cls.User = get_user_model()

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='')

    def test_valid_email_create_user(self):
        user1 = self.User.objects.create_user(
            email='test@gmail.com', password='asdf7890')
        user2 = get_user_model().objects.get(email='test@gmail.com')
        self.assertEqual(user1, user2)
        self.assertFalse(user1.is_superuser)
        self.assertFalse(user1.is_staff)

    def test_valid_email_create_superuser(self):
        user1 = self.User.objects.create_superuser(
            email='test@gmail.com', password='asdf7890')
        self.assertTrue(user1.is_staff)
        self.assertTrue(user1.is_superuser)
