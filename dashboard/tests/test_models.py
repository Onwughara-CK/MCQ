from datetime import timedelta

from django.test import TestCase, Client
# from django.db import models as django_models
from django.urls import reverse
from django.contrib.auth import get_user_model

from dashboard import models


class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up unmodifiable test data
        cls.quiz = models.Quiz.objects.create(
            quiz_title='title 1',
            quiz_text='text 1',
            duration=timedelta(minutes=25)
        )

    def test_quiz_title_label(self):
        field_label = self.quiz._meta.get_field('quiz_title').verbose_name
        self.assertEqual(field_label, 'quiz title')

    def test_quiz_text_label(self):
        field_label = self.quiz._meta.get_field('quiz_text').verbose_name
        self.assertEqual(field_label, 'quiz text')

    def test_duration_label(self):
        field_label = self.quiz._meta.get_field('duration').verbose_name
        self.assertEqual(field_label, 'duration')

    def test_quiz_title_max_length(self):
        max_length = self.quiz._meta.get_field('quiz_title').max_length
        self.assertEqual(max_length, 100)

    def test_duration_default(self):
        default = self.quiz._meta.get_field('duration').default
        self.assertEqual(default, timedelta(minutes=5))

    def test_get_absolute_url(self):
        self.assertEqual(self.quiz.get_absolute_url(),
                         f'/dashboard/quiz/{self.quiz.pk}/')

    def test_get_delete_url(self):
        self.assertEqual(self.quiz.get_delete_url(),
                         f'/dashboard/quiz/{self.quiz.pk}/delete/')

    def test_get_update_url(self):
        self.assertEqual(self.quiz.get_update_url(),
                         f'/dashboard/quiz/{self.quiz.pk}/update/')

    def test_str(self):
        self.assertEqual(str(self.quiz), self.quiz.quiz_title)


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up unmodifiable test data
        cls.quiz = models.Quiz.objects.create(
            quiz_title='title 1',
            quiz_text='text 1',
            duration=timedelta(minutes=25)
        )

        cls.question = models.Question.objects.create(
            question_text='text 1',
            quiz=cls.quiz,
        )

    def test_question_text_label(self):
        field_label = self.question._meta.get_field(
            'question_text').verbose_name
        self.assertEqual(field_label, 'question text')

    def test_quiz_label(self):
        field_label = self.question._meta.get_field('quiz').verbose_name
        self.assertEqual(field_label, 'quiz')

    def test_get_absolute_url(self):
        self.assertEqual(self.question.get_absolute_url(),
                         f'/dashboard/question/{self.question.pk}/')

    def test_get_delete_url(self):
        self.assertEqual(self.question.get_delete_url(),
                         f'/dashboard/question/{self.question.pk}/delete/')

    def test_get_update_url(self):
        self.assertEqual(self.question.get_update_url(),
                         f'/dashboard/question/{self.question.pk}/update/')

    def test_question_foreign_key_relationship_with_quiz(self):
        self.assertEqual(self.quiz.questions.count(), 1)
        self.assertEqual(self.quiz.questions.first().pk, self.question.pk)
        self.assertEqual(str(self.question.quiz), str(self.quiz))

    def test_question_foreign_key_related_model(self):
        self.assertEqual(self.question._meta.get_field(
            'quiz').related_model, models.Quiz)

    def test_str(self):
        self.assertEqual(str(self.question), self.question.question_text)


class ChoiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up unmodifiable test data
        cls.quiz = models.Quiz.objects.create(
            quiz_title='title 1',
            quiz_text='text 1',
            duration=timedelta(minutes=25)
        )

        cls.question = models.Question.objects.create(
            question_text='text 1',
            quiz=cls.quiz,
        )

        cls.choice = models.Choice.objects.create(
            choice_text='text 1',
            question=cls.question,
        )

        cls.MARK = (
            ('right', 'Right'),
            ('wrong', 'Wrong'),
        )

    def test_choice_text_label(self):
        field_label = self.choice._meta.get_field(
            'choice_text').verbose_name
        self.assertEqual(field_label, 'choice text')

    def test_choice_text_max_length(self):
        max_length = self.choice._meta.get_field('choice_text').max_length
        self.assertEqual(max_length, 250)

    def test_question_label(self):
        field_label = self.choice._meta.get_field('question').verbose_name
        self.assertEqual(field_label, 'question')

    def test_mark_label(self):
        field_label = self.choice._meta.get_field('mark').verbose_name
        self.assertEqual(field_label, 'mark')

    def test_mark_max_length(self):
        max_length = self.choice._meta.get_field('mark').max_length
        self.assertEqual(max_length, 5)

    def test_mark_default(self):
        default = self.choice._meta.get_field('mark').default
        self.assertEqual(default, 'wrong')

    def test_mark_choices(self):
        choices = self.choice._meta.get_field('mark').choices
        self.assertEqual(choices, self.MARK)

    def test_get_update_url(self):
        self.assertEqual(self.choice.get_update_url(),
                         f'/dashboard/choice/{self.choice.pk}/update/')

    def test_choice_foreign_key_relationship_with_question(self):
        self.assertEqual(self.question.choices.count(), 1)
        self.assertEqual(self.question.choices.first().pk, self.choice.pk)
        self.assertEqual(str(self.choice.question), str(self.question))

    def test_choice_foreign_key_related_model(self):
        self.assertEqual(self.choice._meta.get_field(
            'question').related_model, models.Question)

    def test_str(self):
        self.assertEqual(str(self.choice), self.choice.choice_text)
