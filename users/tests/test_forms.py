from django.test import TestCase

from users.forms import RegisterForm


class RegisterFormTest(TestCase):
    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            'email': 'test@test.com',
            'password1': 'nklsjiaskljnishujippaodjije2211m2k2m11',
            'password2': 'nklsjiaskljnishujippaodjije2211m2k2m11',
            'teacher': False

        })

        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        form = RegisterForm()
        self.assertFalse(form.is_valid())

    def test_correct_form_fields(self):
        form = RegisterForm()
        self.assertIsNotNone(form.fields.get('email', None))
        self.assertIsNotNone(form.fields.get('teacher', None))
        self.assertIsNotNone(form.fields.get('password1', None))
        self.assertIsNotNone(form.fields.get('password2', None))

    def test_wrong_form_fields(self):
        form = RegisterForm()
        self.assertIsNone(form.fields.get('bar', None))
        self.assertIsNone(form.fields.get('foo', None))
        self.assertIsNone(form.fields.get('foo_bar', None))

    def test_no_of_form_fields(self):
        form = RegisterForm()
        self.assertEqual(len(form.fields), 4)
