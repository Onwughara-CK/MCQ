from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from dashboard import models


class ExamListViewTest(TestCase):
    """
    Test Exam List View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

        ### create 10 quizzes ###
        for i in range(1, 11):
            models.Quiz.objects.create(
                quiz_title=f'title {i}', quiz_text=f'text {i}')

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(reverse('exam:exam-list'))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('exam:exam-list'))
        self.assertRedirects(response, '/login/?next=/exam/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'exam/exam_list.html')

    def test_context_object(self):
        self.assertIn('exams', self.response.context)
        self.assertContains(self.response, 'title 10')
        self.assertCountEqual(
            self.response.context['exams'], models.Quiz.objects.all())


class ExamInstructionsViewTest(TestCase):
    """
    Test Exam Instruction View
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

        ### create Quiz ###
        cls.quiz = models.Quiz.objects.create(
            quiz_title='title 1', quiz_text='text 1')

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(
            reverse('exam:exam-instruction', args=[self.quiz.pk]))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(
            reverse('exam:exam-instruction', args=[self.quiz.pk]))
        self.assertRedirects(
            response, f'/login/?next=/exam/{self.quiz.pk}/instructions/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_correct_template(self):
        self.assertTemplateUsed(self.response, 'exam/exam_instructions.html')


class ExamQuestionsListViewTest(TestCase):
    """
    Test Exam Questions List View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

        ### create Quiz ###
        cls.quiz = models.Quiz.objects.create(
            quiz_title='title 1', quiz_text='text 1')

        ### create 10 questions ###
        for i in range(1, 11):
            models.Question.objects.create(
                question_text=f'question text {i}', quiz=cls.quiz)

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(
            reverse('exam:exam-questions-list', args=[self.quiz.pk]))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(
            reverse('exam:exam-questions-list', args=[self.quiz.pk]))
        self.assertRedirects(response, f'/login/?next=/exam/{self.quiz.pk}/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_correct_template(self):
        self.assertTemplateUsed(self.response, 'exam/exam_questions.html')

    def test_context_object(self):
        self.assertEqual(self.response.context['quiz_pk'], self.quiz.pk)
        self.assertIn('questions', self.response.context)

    def test_pagination(self):
        self.assertTrue(self.response.context['is_paginated'])
        self.assertEqual(
            self.response.context['paginator'].count, self.quiz.questions.count())
        self.assertEqual(self.response.context['paginator'].per_page, 1)


class ExamResultViewTest(TestCase):
    """
    Test Exam Result View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

        ### create Quiz ###
        cls.quiz = models.Quiz.objects.create(
            quiz_title='title 1', quiz_text='text 1')

        ### create 10 questions and for choices for each question ###
        for i in range(1, 11):
            cls.question = models.Question.objects.create(
                question_text=f'question text {i}', quiz=cls.quiz)
            for i in range(1, 5):
                if i == 3:
                    models.Choice.objects.create(
                        choice_text=f'choice {i}',
                        mark='right',
                        question=cls.question,
                    )
                models.Choice.objects.create(
                    choice_text=f'choice {i}',
                    mark='wrong',
                    question=cls.question,
                )

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(reverse('exam:exam-result'))

    # test not login
    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('exam:exam-result'))
        self.assertRedirects(response, f'/login/?next=/exam/result/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_but_not_ajax(self):
        self.assertEqual(self.response.status_code, 404)
        # post
        response = self.client.post(reverse('exam:exam-result'))
        self.assertEqual(response.status_code, 204)

    def test_logged_in_with_ajax_get(self):
        response = self.client.get(
            reverse('exam:exam-result'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        # receive json bytes, so decode byte to json and check
        self.assertJSONEqual(response.content.decode(), {})

    # test post as ajax without finish
    def test_logged_in_with_ajax_post_not_finish(self):
        response = self.client.post(
            reverse('exam:exam-result'),
            data={},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 204)

    def test_logged_in_with_ajax_post_and_finish(self):
        response = self.client.post(
            reverse('exam:exam-result'),
            data={
                'finish': True,
                'quiz_pk': self.quiz.pk,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 404)

    def test_logged_in_without_ajax_post_but_finish(self):
        response = self.client.post(
            reverse('exam:exam-result'),
            data={
                'finish': True,
                'quiz_pk': self.quiz.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exam/result_sheet.html')
        self.assertEqual(response.context['no_of_questions'], 10)
        self.assertEqual(response.context['no_of_correct_choices_answered'], 0)
        self.assertEqual(response.context['no_of_questions_answered'], 0)
        self.assertEqual(response.context['score_percent'], 0)

    def test_logged_in_without_ajax_post_and_finish_with_correct_choices(self):
        response = self.client.post(
            reverse('exam:exam-result'),
            data={
                'finish': True,
                'quiz_pk': self.quiz.pk,
                'Question1': models.Choice.objects.filter(mark='right').first().pk,
                'Question2': models.Choice.objects.filter(mark='right').last().pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exam/result_sheet.html')
        self.assertEqual(response.context['no_of_questions'], 10)
        self.assertEqual(response.context['no_of_correct_choices_answered'], 2)
        self.assertEqual(response.context['no_of_questions_answered'], 2)
        self.assertEqual(response.context['score_percent'], 20)


# test ajax get and post
# test quiz duration, create quiz and send pk
# test 404 with wrong pk
class ExamTimerViewTest(TestCase):
    """
    Test Exam Timer View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

        ### create Quiz ###
        cls.quiz = models.Quiz.objects.create(
            quiz_title='title 1', quiz_text='text 1', duration=timedelta(minutes=25))

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(reverse('exam:timer'))

    def test_not_ajax(self):
        self.assertEqual(self.response.status_code, 404)
        # post
        response = self.client.post(reverse('exam:timer'))
        self.assertEqual(response.status_code, 404)

    def test_with_ajax_get(self):
        response = self.client.get(
            reverse('exam:timer'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_ajax_post_with_invalid_data(self):
        response = self.client.post(
            reverse('exam:timer'),
            data={},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 404)

    def test_logged_in_with_ajax_post_with_valid_data(self):
        response = self.client.post(
            reverse('exam:timer'),
            data={
                'pk': self.quiz.pk,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )        
        self.assertEqual(response.status_code, 200)
