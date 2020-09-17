from datetime import timedelta

from django.test import SimpleTestCase

from dashboard import forms


class QuizFormTest(SimpleTestCase):
    def test_valid_data(self):
        data = {
            'duration': timedelta(minutes=30),
            'quiz_title': 'title 1',
            'quiz_text': 'text 1',
        }

        form = forms.QuizForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        data = {}
        form = forms.QuizForm(data)
        self.assertFalse(form.is_valid())

    def test_correct_form_fields(self):
        form = forms.QuizForm()
        self.assertIsNotNone(form.fields.get('duration', None))
        self.assertIsNotNone(form.fields.get('quiz_title', None))
        self.assertIsNotNone(form.fields.get('quiz_text', None))

    def test_wrong_form_fields(self):
        form = forms.QuizForm()
        self.assertIsNone(form.fields.get('bar', None))
        self.assertIsNone(form.fields.get('foo', None))
        self.assertIsNone(form.fields.get('foo_bar', None))

    def test_no_of_form_fields(self):
        form = forms.QuizForm()
        self.assertEqual(len(form.fields), 3)


class QuestionFormTest(SimpleTestCase):
    def test_valid_data(self):
        data = {
            'question_text': 'text 1',
        }

        form = forms.QuestionForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        data = {}
        form = forms.QuestionForm(data)
        self.assertFalse(form.is_valid())

    def test_correct_form_fields(self):
        form = forms.QuestionForm()
        self.assertIsNotNone(form.fields.get('question_text', None))

    def test_wrong_form_fields(self):
        form = forms.QuestionForm()
        self.assertIsNone(form.fields.get('bar', None))
        self.assertIsNone(form.fields.get('foo', None))

    def test_no_of_form_fields(self):
        form = forms.QuestionForm()
        self.assertEqual(len(form.fields), 1)


class ChoiceFormTest(SimpleTestCase):
    def test_valid_data(self):
        data = {
            'choice_text': 'choice 1',
            'mark': 'wrong',
        }

        form = forms.ChoiceForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        data = {}
        form = forms.ChoiceForm(data)
        self.assertFalse(form.is_valid())

    def test_correct_form_fields(self):
        form = forms.ChoiceForm()
        self.assertIsNotNone(form.fields.get('choice_text', None))
        self.assertIsNotNone(form.fields.get('mark', None))

    def test_wrong_form_fields(self):
        form = forms.ChoiceForm()
        self.assertIsNone(form.fields.get('bar', None))
        self.assertIsNone(form.fields.get('foo', None))

    def test_no_of_form_fields(self):
        form = forms.ChoiceForm()
        self.assertEqual(len(form.fields), 2)
