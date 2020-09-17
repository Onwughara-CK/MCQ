from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from dashboard import models


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
