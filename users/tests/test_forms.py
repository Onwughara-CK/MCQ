from django.test import TestCase
from users.forms import RegisterForm


class FormTest(TestCase):
    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            'email': 'test@test.com',
            'password1': 'nklsjiaskljnishujippaodjije2211m2k2m11',
            'password2': 'nklsjiaskljnishujippaodjije2211m2k2m11',

        })

        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        form = RegisterForm()
        self.assertFalse(form.is_valid())
