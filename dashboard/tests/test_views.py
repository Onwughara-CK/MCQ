from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils.dateparse import parse_duration

from dashboard import models


class DashViewTest(TestCase):
    """
    Test Dash View
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create student ###
        cls.student = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dash:dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dash.html')


class QuizListViewTest(TestCase):
    """
    Test Quiz List View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create student ###
        cls.student = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dash:quiz-list'))
        self.assertRedirects(response, '/login/?next=/dashboard/quizzes/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-list'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-list'))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/quiz_list.html')

    def test_context_object_name(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-list'))
        self.assertTrue('quizzes' in response.context)


class QuizDetailViewTest(TestCase):
    """
    Test Quiz Detail View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create student ###
        cls.student = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dash:quiz-detail', args=[1]))
        self.assertRedirects(response, '/login/?next=/dashboard/quiz/1/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-detail', args=[quiz.pk]))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-detail', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-detail', args=[quiz.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/quiz_detail.html')

    def test_context_object_name(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-detail', args=[quiz.pk]))
        self.assertTrue('quiz' in response.context)


class QuizDeleteViewTest(TestCase):
    """
    Test Quiz Delete View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create student ###
        cls.student = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

    def test_redirect_if_not_logged_in(self):
        response_get = self.client.get(reverse('dash:quiz-delete', args=[1]))
        response_delete = self.client.delete(
            reverse('dash:quiz-delete', args=[1]))
        self.assertRedirects(
            response_get, '/login/?next=/dashboard/quiz/1/delete/')
        self.assertRedirects(
            response_delete, '/login/?next=/dashboard/quiz/1/delete/')
        self.assertEqual(response_get.status_code, 302)
        self.assertEqual(response_delete.status_code, 302)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(reverse('dash:quiz-delete', args=[1]))
        response_delete = self.client.delete(
            reverse('dash:quiz-delete', args=[1]))
        self.assertEqual(response_delete.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:quiz-delete', args=[quiz.pk]))
        # redirects to confirm delete template
        self.assertEqual(response_get.status_code, 200)

        response_delete = self.client.delete(
            reverse('dash:quiz-delete', args=[quiz.pk]))
        self.assertEqual(response_delete.status_code,
                         302)  # redirects after delete
        self.assertFalse(models.Quiz.objects.filter(
            pk=quiz.pk).exists())  # check if the deleted item still exists

    def test_returns_correct_confirm_delete_template(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-delete', args=[quiz.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/quiz_confirm_delete.html')

    def test_context_object_name(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-delete', args=[quiz.pk]))
        self.assertTrue('quiz' in response.context)

    def test_success_message(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.delete(
            reverse('dash:quiz-delete', args=[quiz.pk]))
        # no context data as it redirects
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully Deleted quiz')


class QuizUpdateViewTest(TestCase):
    """
    Test Quiz Update View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        ### create student ###
        cls.student = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

        ### create teacher ###
        cls.teacher = get_user_model().objects.create_user(
            email='teacher@test.com', password='asdf7890',)
        cls.teacher.teacher = True
        cls.teacher.save()

    def test_redirect_if_not_logged_in(self):
        response_get = self.client.get(reverse('dash:quiz-update', args=[1]))
        response_put = self.client.put(
            reverse('dash:quiz-update', args=[1]))
        self.assertRedirects(
            response_get, '/login/?next=/dashboard/quiz/1/update/')
        self.assertRedirects(
            response_put, '/login/?next=/dashboard/quiz/1/update/')
        self.assertEqual(response_get.status_code, 302)
        self.assertEqual(response_put.status_code, 302)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(reverse('dash:quiz-update', args=[1]))
        response_put = self.client.put(
            reverse('dash:quiz-update', args=[1]))
        self.assertEqual(response_put.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:quiz-update', args=[quiz.pk]))
        self.assertEqual(response_get.status_code, 200)
        response_put = self.client.post(
            path=reverse('dash:quiz-update', args=[quiz.pk]),
            data={
                'quiz_text': 'text updated',
                'duration':    timedelta(minutes=30),
                'quiz_title': 'title updated',
            }
        )  # use client.post instead of client.put
        self.assertEqual(response_put.status_code,
                         302)  # redirects after update
        quiz.refresh_from_db()
        self.assertEqual(quiz.quiz_text, 'text updated')
        self.assertEqual(quiz.quiz_title, 'title updated')
        self.assertEqual(quiz.duration, timedelta(minutes=30))

    def test_success_message(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.post(
            reverse('dash:quiz-update', args=[quiz.pk]),
            {
                'quiz_text': 'text updated',
                'duration':    timedelta(minutes=30),
                'quiz_title': 'title updated',
            }
        )
        # no context data as it redirects
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully Updated quiz')
