from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

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

        ### create 10 quizzes ###
        for i in range(1, 11):
            models.Quiz.objects.create(
                quiz_title=f'title {i}', quiz_text=f'text {i}')

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

    def test_context_object(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-list'))
        self.assertTrue('quizzes' in response.context)
        self.assertContains(response, 'title 10')
        self.assertCountEqual(
            response.context['quizzes'], models.Quiz.objects.all())


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

    def test_context_object(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz-detail', args=[quiz.pk]))
        self.assertTrue('quiz' in response.context)
        self.assertContains(response, 'title')


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


class QuestionListViewTest(TestCase):
    """
    Test Question List View
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

        ### create 10 questions ###
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        for i in range(1, 11):
            models.Question.objects.create(
                question_text=f'text {i}', quiz=quiz)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dash:question-list'))
        self.assertRedirects(response, '/login/?next=/dashboard/questions/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:question-list'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:question-list'))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:question-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/question_list.html')

    def test_context_object(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:question-list'))
        self.assertTrue('questions' in response.context)
        self.assertContains(response, 'text 10')
        self.assertCountEqual(
            response.context['questions'], models.Question.objects.all())


class QuestionDetailViewTest(TestCase):
    """
    Test Question Detail View
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
        response = self.client.get(reverse('dash:question-detail', args=[1]))
        self.assertRedirects(response, '/login/?next=/dashboard/question/1/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(email='teacher@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:question-detail', args=[question.pk]))
        self.assertEqual(response.status_code, 200)

    def test_returns_correct_template(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:question-detail', args=[question.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/question_detail.html')

    def test_context_object_name(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:question-detail', args=[question.pk]))
        self.assertTrue('question' in response.context)


class QuestionDeleteViewTest(TestCase):
    """
    Test Question Delete View
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
        response_get = self.client.get(
            reverse('dash:question-delete', args=[1]))
        response_delete = self.client.delete(
            reverse('dash:question-delete', args=[1]))
        self.assertRedirects(
            response_get, '/login/?next=/dashboard/question/1/delete/')
        self.assertRedirects(
            response_delete, '/login/?next=/dashboard/question/1/delete/')
        self.assertEqual(response_get.status_code, 302)
        self.assertEqual(response_delete.status_code, 302)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:question-delete', args=[1]))
        response_delete = self.client.delete(
            reverse('dash:question-delete', args=[1]))
        self.assertEqual(response_delete.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:question-delete', args=[question.pk]))
        # redirects to confirm delete template
        self.assertEqual(response_get.status_code, 200)

        response_delete = self.client.delete(
            reverse('dash:question-delete', args=[question.pk]))
        self.assertEqual(response_delete.status_code,
                         302)  # redirects after delete
        self.assertFalse(models.Question.objects.filter(
            pk=question.pk).exists())  # check if the deleted item still exists

    def test_returns_correct_confirm_delete_template(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:question-delete', args=[question.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'dashboard/question_confirm_delete.html')

    def test_context_object_name(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:question-delete', args=[question.pk]))
        self.assertTrue('question' in response.context)

    def test_success_message(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.delete(
            reverse('dash:question-delete', args=[question.pk]))
        # no context data as it redirects
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully Deleted Question')


class QuestionUpdateViewTest(TestCase):
    """
    Test Question Update View
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
        response_get = self.client.get(
            reverse('dash:question-update', args=[1]))
        response_put = self.client.put(
            reverse('dash:question-update', args=[1]))
        self.assertRedirects(
            response_get, '/login/?next=/dashboard/question/1/update/')
        self.assertRedirects(
            response_put, '/login/?next=/dashboard/question/1/update/')
        self.assertEqual(response_get.status_code, 302)
        self.assertEqual(response_put.status_code, 302)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:question-update', args=[1]))
        response_put = self.client.put(
            reverse('dash:question-update', args=[1]))
        self.assertEqual(response_put.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:question-update', args=[question.pk]))
        self.assertEqual(response_get.status_code, 200)
        response_put = self.client.post(
            path=reverse('dash:question-update', args=[question.pk]),
            data={
                'question_text': 'text updated',
            }
        )  # use client.post instead of client.put
        self.assertEqual(response_put.status_code,
                         302)  # redirects after update
        question.refresh_from_db()
        self.assertEqual(question.question_text, 'text updated')

    def test_success_message(self):
        quiz = models.Quiz.objects.create(quiz_text='text', quiz_title='title')
        question = models.Question.objects.create(
            question_text='text', quiz=quiz)
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.post(
            reverse('dash:question-update', args=[question.pk]),
            {
                'question_text': 'text updated',
            }
        )
        # no context data as it redirects
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully Updated Question')


class QuizQuestionsListViewTest(TestCase):
    """
    Test Quiz Questions List View
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

        ### create 10 questions for quiz###
        cls.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')
        for i in range(1, 11):
            models.Question.objects.create(
                question_text=f'text {i}', quiz=cls.quiz)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('dash:quiz-questions', args=[self.quiz.pk]))
        self.assertRedirects(
            response, '/login/?next=/dashboard/quiz/1/questions/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:quiz-questions', args=[self.quiz.pk]))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        _ = self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:quiz-questions', args=[self.quiz.pk]))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:quiz-questions', args=[self.quiz.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/quiz_question_list.html')

    def test_context_object(self):
        _ = self.client.login(
            email='teacher@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:quiz-questions', args=[self.quiz.pk]))
        self.assertTrue('questions' in response.context)
        self.assertCountEqual(
            response.context['questions'], self.quiz.questions.all())
