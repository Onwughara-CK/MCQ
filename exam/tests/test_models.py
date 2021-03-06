from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from exam import models
from dashboard.models import Quiz


class ExamResultListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up unmodifiable test data
        ### create student ###
        cls.student = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890'
        )

        cls.quiz = Quiz.objects.create(
                quiz_title='title 1', 
                quiz_text='text 1',
            )

        cls.result = models.Result.objects.create(
            percentage=77,
            time_spent=timedelta(minutes=12),
            no_of_questions_answered=8,
            no_of_correct_choices_answered=5,
            no_of_questions=8,
            user = cls.student,
            quiz = cls.quiz
        )

        cls.result1 = models.Result.objects.create(
            percentage=77,
            time_spent=timedelta(minutes=10),
            no_of_questions_answered=6,
            no_of_correct_choices_answered=5,
            no_of_questions=10,
            user = cls.student,
            quiz = cls.quiz
        )        

    def test_percentage_label(self):
        field_label = self.result._meta.get_field(
            'percentage').verbose_name
        self.assertEqual(field_label, 'percentage')

    def test_time_spent_label(self):
        field_label = self.result._meta.get_field('time_spent').verbose_name
        self.assertEqual(field_label, 'time spent')

    def test_failed_label(self):
        field_label = self.result._meta.get_field('no_of_questions_answered').verbose_name
        self.assertEqual(field_label, 'no of questions answered')

    def test_passed_label(self):
        field_label = self.result._meta.get_field('no_of_correct_choices_answered').verbose_name
        self.assertEqual(field_label, 'no of correct choices answered')

    def test_no_of_questions_label(self):
        field_label = self.result._meta.get_field('no_of_questions').verbose_name
        self.assertEqual(field_label, 'no of questions')

    def test_user_label(self):
        field_label = self.result._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_percentage_default(self):
        default = self.result._meta.get_field('percentage').default
        self.assertEqual(default, 0)

    def test_time_spent_default(self):
        default = self.result._meta.get_field('time_spent').default
        self.assertEqual(default, 0)

    def test_failed_default(self):
        default = self.result._meta.get_field('no_of_questions_answered').default
        self.assertEqual(default, 0)

    def test_passed_default(self):
        default = self.result._meta.get_field('no_of_correct_choices_answered').default
        self.assertEqual(default, 0)

    def test_no_of_questions_default(self):
        default = self.result._meta.get_field('no_of_questions').default
        self.assertEqual(default, 0)    

    def test_result_foreign_key_relationship_with_student(self):
        self.assertEqual(self.student.results.count(), 2)
        self.assertEqual(str(self.result.user), str(self.student))

    def test_result_foreign_key_related_user_model(self):
        self.assertEqual(self.result._meta.get_field(
            'user').related_model, get_user_model())

    def test_result_foreign_key_relationship_with_quiz(self):
        self.assertEqual(self.quiz.results.count(), 2)
        self.assertEqual(str(self.result.quiz), str(self.quiz))

    def test_result_foreign_key_related_quiz_model(self):
        self.assertEqual(self.result._meta.get_field(
            'quiz').related_model, Quiz)

    def test_str(self):
        self.assertEqual(str(self.result), str(self.result.percentage))
