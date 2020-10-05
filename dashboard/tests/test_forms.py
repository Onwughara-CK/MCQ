from datetime import timedelta

from django.forms import formset_factory
from django.test import SimpleTestCase, TestCase
from django import forms as dj_forms
from django.core.exceptions import ValidationError


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


class BaseChoiceFormSetTest(TestCase):
     # set up test data
    @classmethod
    def setUpTestData(cls):
        cls.ChoiceFormSet = formset_factory(
                                        forms.ChoiceForm,
                                        extra=4, 
                                        max_num=4, 
                                        formset=forms.BaseChoiceFormSet,
                                        can_delete=True,
                            )

    # set up modifables
    def setUp(self):
        self.data = {
                'form-0-choice_text': 'choice0',
                'form-1-choice_text': 'choice1',
                'form-2-choice_text': 'choice2',
                'form-3-choice_text': 'choice3',
                'form-0-mark': 'wrong',
                'form-1-mark': 'wrong',
                'form-2-mark': 'wrong',
                'form-3-mark': 'wrong',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MAX_NUM_FORMS': 4,
                'form-MIN_NUM_FORMS': 0,
        }
    

    def test_valid_data(self):        
        formset = self.ChoiceFormSet(self.data)
        self.assertTrue(formset.is_valid())

    def test_invalid_data(self):
        data = {                
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MAX_NUM_FORMS': 4,
                'form-MIN_NUM_FORMS': 0,
            }
        formset = self.ChoiceFormSet(data)
        self.assertFalse(formset.is_valid())
        self.assertEqual(formset.clean(),None) #if any form has error

    def test_two_choices_with_same_text(self):
        self.data['form-0-choice_text']= 'choice1' #make choice 0 text equal to choice 1 text
        formset = self.ChoiceFormSet(self.data)
        self.assertFalse(formset.is_valid())            
        with self.assertRaisesMessage(
            ValidationError,
            'choices in a question set must have distinct text.'):
            formset.clean()            

    def test_no_two_choices_with_same_text(self):            
        formset = self.ChoiceFormSet(self.data)
        self.assertIsNone(formset.clean())

    def test_can_delete_true_and_should_delete_form_true(self):
        self.data['form-0-DELETE'] = 'on'
        self.data['form-1-DELETE'] = 'on'
        self.data['form-2-DELETE'] = 'on'
        self.data['form-3-DELETE'] = 'on'
        formset = self.ChoiceFormSet(self.data)
        self.assertIsNone(formset.clean())

    def test_can_delete_false_and_should_delete_form_false(self):
        self.data['form-0-DELETE'] = ''
        self.data['form-1-DELETE'] = ''
        self.data['form-2-DELETE'] = ''
        self.data['form-3-DELETE'] = ''
        formset = self.ChoiceFormSet(self.data)
        self.assertIsNone(formset.clean())




            