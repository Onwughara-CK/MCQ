from datetime import timedelta

from django.test import TestCase, Client
from django.db import models as django_models
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
