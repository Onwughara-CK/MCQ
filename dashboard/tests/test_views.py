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

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(reverse('dash:dashboard'))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('dash:dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response.status_code, 200)

    # def test_logged_in_but_not_correct_permission(self):
    #     self.client.login(
    #         email='student@test.com', password='asdf7890')
    #     response = self.client.get(reverse('dash:dashboard'))
    #     self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        self.assertTemplateUsed(self.response, 'dashboard/dash.html')


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
        self.response = self.client.get(reverse('dash:quiz_list'))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('dash:quiz_list'))
        self.assertRedirects(response, '/login/?next=/dashboard/quizzes/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:quiz_list'))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'dashboard/quiz_list.html')

    def test_context_object(self):
        self.assertTrue('quizzes' in self.response.context)
        self.assertContains(self.response, 'title 10')
        self.assertCountEqual(
            self.response.context['quizzes'], models.Quiz.objects.all())


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

        ### create quiz ###
        cls.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(
            reverse('dash:quiz-detail', args=[self.quiz.pk]))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(
            reverse('dash:quiz-detail', args=[self.quiz.pk]))
        self.assertRedirects(response, '/login/?next=/dashboard/quiz/1/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:quiz-detail', args=[self.quiz.pk]))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'dashboard/quiz_detail.html')

    def test_context_object(self):
        self.assertTrue('quiz' in self.response.context)
        self.assertContains(self.response, 'title')


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

    def setUp(self):
        ### create quiz ###
        self.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')

        self.client.login(
            email='teacher@test.com', password='asdf7890')

        self.response_get = self.client.get(
            reverse('dash:quiz-delete', args=[self.quiz.pk]))

        self.response_delete = self.client.delete(
            reverse('dash:quiz-delete', args=[self.quiz.pk]))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
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
        self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(reverse('dash:quiz-delete', args=[1]))
        response_delete = self.client.delete(
            reverse('dash:quiz-delete', args=[1]))
        self.assertEqual(response_delete.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        # returns confirm delete template
        self.assertEqual(self.response_get.status_code, 200)
        # redirects after delete
        self.assertEqual(self.response_delete.status_code, 302)
        # check if the deleted item still exists
        self.assertFalse(models.Quiz.objects.filter(pk=self.quiz.pk).exists())

    def test_returns_correct_confirm_delete_template(self):
        self.assertEqual(self.response_get.status_code, 200)
        self.assertTemplateUsed(
            self.response_get, 'dashboard/dash_confirm_delete.html')

    def test_context_object_name(self):
        self.assertTrue('object' in self.response_get.context)

    def test_success_message(self):
        # no context data as it redirects
        messages = list(get_messages(self.response_delete.wsgi_request))
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

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')
        self.response_get = self.client.get(
            reverse('dash:quiz-update', args=[self.quiz.pk]))
        self.response_put = self.client.post(
            path=reverse('dash:quiz-update', args=[self.quiz.pk]),
            data={
                'quiz_text': 'text updated',
                'duration':    timedelta(minutes=30),
                'quiz_title': 'title updated',
            }
        )

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
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
        self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(reverse('dash:quiz-update', args=[1]))
        response_put = self.client.put(
            reverse('dash:quiz-update', args=[1]))
        self.assertEqual(response_put.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response_get.status_code, 200)
        # use client.post instead of client.put
        self.assertEqual(self.response_put.status_code,
                         302)  # redirects after update
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.quiz_text, 'text updated')
        self.assertEqual(self.quiz.quiz_title, 'title updated')
        self.assertEqual(self.quiz.duration, timedelta(minutes=30))

    def test_success_message(self):
        # no context data as it redirects
        messages = list(get_messages(self.response_put.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully Updated quiz')

    def test_invalid_data(self):
        response_put = self.client.post(
            path=reverse('dash:quiz-update', args=[self.quiz.pk]),
            data={}
        )
        # meant to redirect with status code 302 not 200
        self.assertEqual(response_put.status_code, 200)


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

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(reverse('dash:question-list'))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('dash:question-list'))
        self.assertRedirects(response, '/login/?next=/dashboard/questions/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(reverse('dash:question-list'))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'dashboard/question_list.html')

    def test_context_object(self):
        self.assertTrue('questions' in self.response.context)
        self.assertContains(self.response, 'text 10')
        self.assertCountEqual(
            self.response.context['questions'], models.Question.objects.all())


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

        ### create question ###
        cls.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')
        cls.question = models.Question.objects.create(
            question_text='text', quiz=cls.quiz)

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(
            reverse('dash:question-detail', args=[self.question.pk]))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('dash:question-detail', args=[1]))
        self.assertRedirects(response, '/login/?next=/dashboard/question/1/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, 'dashboard/question_detail.html')

    def test_context_object_name(self):
        self.assertTrue('question' in self.response.context)


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

    def setUp(self):
        ### create question ###
        self.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')

        self.question = models.Question.objects.create(
            question_text='text', quiz=self.quiz)

        self.client.login(
            email='teacher@test.com', password='asdf7890')

        self.response_get = self.client.get(
            reverse('dash:question-delete', args=[self.question.pk]))

        self.response_delete = self.client.delete(
            reverse('dash:question-delete', args=[self.question.pk]))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
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
        self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:question-delete', args=[1]))
        response_delete = self.client.delete(
            reverse('dash:question-delete', args=[1]))
        self.assertEqual(response_delete.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        # redirects to confirm delete template
        self.assertEqual(self.response_get.status_code, 200)
        self.assertEqual(self.response_delete.status_code,
                         302)  # redirects after delete
        self.assertFalse(models.Question.objects.filter(
            pk=self.question.pk).exists())  # check if the deleted item still exists

    def test_returns_correct_confirm_delete_template(self):
        self.assertEqual(self.response_get.status_code, 200)
        self.assertTemplateUsed(
            self.response_get, 'dashboard/dash_confirm_delete.html')

    def test_context_object_name(self):
        self.assertTrue('object' in self.response_get.context)

    def test_success_message(self):
        # no context data as it redirects
        messages = list(get_messages(self.response_delete.wsgi_request))
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

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')
        self.question = models.Question.objects.create(
            question_text='text', quiz=self.quiz)
        self.response_get = self.client.get(
            reverse('dash:question-update', args=[self.question.pk]))
        self.response_put = self.client.post(
            path=reverse('dash:question-update', args=[self.question.pk]),
            data={
                'question_text': 'text updated',
            }
        )

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
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
        self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:question-update', args=[1]))
        response_put = self.client.put(
            reverse('dash:question-update', args=[1]))
        self.assertEqual(response_put.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response_put.status_code,
                         302)  # redirects after update
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, 'text updated')

    def test_success_message(self):
        # no context data as it redirects
        messages = list(get_messages(self.response_put.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully Updated Question')

    def test_invalid_data(self):
        response_post = self.client.post(
            path=reverse('dash:question-update', args=[self.question.pk]),
            data={}
        )
        # should redirect with status code 302 not 200
        self.assertEqual(response_post.status_code, 200)


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

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(
            reverse('dash:quiz-questions', args=[self.quiz.pk]))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(
            reverse('dash:quiz-questions', args=[self.quiz.pk]))
        self.assertRedirects(
            response, '/login/?next=/dashboard/quiz/1/questions/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response.status_code, 200)

    def test_logged_in_but_not_correct_permission(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response = self.client.get(
            reverse('dash:quiz-questions', args=[self.quiz.pk]))
        self.assertEqual(response.status_code, 403)

    def test_returns_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, 'dashboard/quiz_question_list.html')

    def test_context_object(self):
        self.assertTrue('quiz' in self.response.context)
        self.assertCountEqual(
            self.response.context['quiz'].questions.all(), self.quiz.questions.all())


class ChoiceUpdateViewTest(TestCase):
    """
    Test Choice Update View
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

    def setUp(self):
        self.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')
        self.question = models.Question.objects.create(
            question_text='text', quiz=self.quiz)
        self.choice = models.Choice.objects.create(
            choice_text='text', question=self.question)
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response_get = self.client.get(
            reverse('dash:choice-update', args=[self.choice.pk]))
        self.response_put = self.client.post(
            reverse('dash:choice-update', args=[self.choice.pk]),
            {
                'mark': 'wrong',
                'choice_text': 'text updated',
            }
        )

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response_get = self.client.get(
            reverse('dash:choice-update', args=[1]))
        response_put = self.client.put(
            reverse('dash:choice-update', args=[1]))
        self.assertRedirects(
            response_get, '/login/?next=/dashboard/choice/1/update/')
        self.assertRedirects(
            response_put, '/login/?next=/dashboard/choice/1/update/')
        self.assertEqual(response_get.status_code, 302)
        self.assertEqual(response_put.status_code, 302)

    def test_logged_in_but_not_correct_permission(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:choice-update', args=[1]))
        response_put = self.client.put(
            reverse('dash:choice-update', args=[1]))
        self.assertEqual(response_put.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response_get.status_code, 200)
        # use client.post instead of client.put
        self.assertEqual(self.response_put.status_code,
                         302)  # redirects after update
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.choice_text, 'text updated')

    def test_success_message(self):
        # no context data as it redirects
        messages = list(get_messages(self.response_put.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully Updated Choice')

    def test_invalid_data(self):
        response_post = self.client.post(
            path=reverse('dash:choice-update', args=[self.choice.pk]),
            data={}
        )
        self.assertEqual(response_post.status_code, 200)


class CreateQuizViewTest(TestCase):
    """
    Test Create Quiz View
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

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response_get = self.client.get(
            reverse('dash:create-quiz'))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response_get = self.client.get(
            reverse('dash:create-quiz'))
        response_post = self.client.post(
            reverse('dash:create-quiz'))
        self.assertRedirects(
            response_get, '/login/?next=/dashboard/create-quiz/')
        self.assertRedirects(
            response_post, '/login/?next=/dashboard/create-quiz/')
        self.assertEqual(response_get.status_code, 302)
        self.assertEqual(response_post.status_code, 302)

    def test_logged_in_but_not_correct_permission(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:create-quiz'))
        response_post = self.client.post(
            reverse('dash:create-quiz'))
        self.assertEqual(response_post.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response_get.status_code, 200)
        self.assertTemplateUsed(
            self.response_get, 'dashboard/create_quiz.html')

        ### test request.POST['finish'] ###
        response_post = self.client.post(
            path=reverse('dash:create-quiz'),
            data={
                'quiz_text': 'quiz text finish',
                'quiz_title': 'quiz title',
                'duration': timedelta(minutes=25),
                'finish': True,
            }
        )
        ### redirects after post ###
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(models.Quiz.objects.get(
            quiz_text='quiz text finish').quiz_text, 'quiz text finish')

        ### test request.POST['finish'] is None ###
        response_post = self.client.post(
            path=reverse('dash:create-quiz'),
            data={
                'quiz_text': 'quiz text',
                'quiz_title': 'quiz title',
                'duration': timedelta(minutes=25),
            }
        )
        self.assertEqual(response_post.status_code, 200)
        self.assertTemplateUsed(response_post, 'dashboard/create_quiz.html')

        ### test request.POST['continue'] ###
        response_post = self.client.post(
            path=reverse('dash:create-quiz'),
            data={
                'quiz_text': 'quiz text continue',
                'quiz_title': 'quiz title',
                'duration': timedelta(minutes=25),
                'continue': True,
            }
        )
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(models.Quiz.objects.get(
            quiz_text='quiz text continue').quiz_text, 'quiz text continue')
        
    def test_invalid_data(self):
        response_post = self.client.post(reverse('dash:create-quiz'), data={})
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(models.Quiz.objects.count(), 0)


class CreateQuestionAndChoiceViewTest(TestCase):
    """
    Test Create Question and Choice View
    """

    # set up test data
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

        ### create quiz ###
        cls.quiz = models.Quiz.objects.create(
            quiz_text='text', quiz_title='title')

    # set up modifables

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response_get = self.client.get(
            reverse('dash:create-question-choice', args=[self.quiz.pk]))

    # test if not login
    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response_get = self.client.get(
            reverse('dash:create-question-choice', args=[self.quiz.pk]))
        response_post = self.client.post(
            reverse('dash:create-question-choice', args=[self.quiz.pk]))
        self.assertRedirects(
            response_get, f'/login/?next=/dashboard/quiz/{self.quiz.pk}/create-question-choice/')
        self.assertRedirects(
            response_post, f'/login/?next=/dashboard/quiz/{self.quiz.pk}/create-question-choice/')
        self.assertEqual(response_get.status_code, 302)
        self.assertEqual(response_post.status_code, 302)

    # test login and render the correct template
    def test_logged_in_with_correct_permission(self):
        self.assertEqual(self.response_get.status_code, 200)
        self.assertTemplateUsed(
            self.response_get, 'dashboard/create_quiz.html')

    # test permission
    def test_logged_in_but_not_correct_permission(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        response_get = self.client.get(
            reverse('dash:create-question-choice', args=[self.quiz.pk]))
        response_post = self.client.post(
            reverse('dash:create-question-choice', args=[self.quiz.pk]))
        self.assertEqual(response_post.status_code, 403)
        self.assertEqual(response_get.status_code, 403)

    # test context for forms
    def test_context_object(self):
        self.assertTrue('form' in self.response_get.context)
        self.assertTrue('formset' in self.response_get.context)
        # check that the no choice forms is 4
        self.assertEqual(len(self.response_get.context['formset']), 4)

    # test only question form is valid
    def test_one_form_valid(self):
        """
        Only question form is valid, so the form is re-rendered
        """
        response_post = self.client.post(
            reverse('dash:create-question-choice', args=[self.quiz.pk]),
            {
                'question_text': 'question text',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MAX_NUM_FORMS': 4,
                'form-MIN_NUM_FORMS': 0,
                'finish': True,
            }
        )
        self.assertEqual(response_post.status_code, 200)
        self.assertTemplateUsed(response_post, 'dashboard/create_quiz.html')

    # test both choice and question forms valid and POST['finish']
    def test_both_forms_valid_and_finish_button_click(self):
        ### create dummy post data ###
        response_post = self.client.post(
            reverse('dash:create-question-choice', args=[self.quiz.pk]),
            {
                'form-0-choice_text': 'choice0',
                'form-1-choice_text': 'choice1',
                'form-2-choice_text': 'choice2',
                'form-3-choice_text': 'choice3',
                'form-0-mark': 'wrong',
                'form-1-mark': 'wrong',
                'form-2-mark': 'wrong',
                'form-3-mark': 'wrong',
                'question_text': 'question text',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MAX_NUM_FORMS': 4,
                'form-MIN_NUM_FORMS': 0,
                'finish': True,
            }
        )
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, f'/dashboard/quiz/{self.quiz.pk}/questions/')

    def test_both_forms_valid_and_continue_button_click(self):
        response_post = self.client.post(
            reverse('dash:create-question-choice', args=[self.quiz.pk]),
            {
                'form-0-choice_text': 'choice0',
                'form-1-choice_text': 'choice1',
                'form-2-choice_text': 'choice2',
                'form-3-choice_text': 'choice3',
                'form-0-mark': 'wrong',
                'form-1-mark': 'wrong',
                'form-2-mark': 'wrong',
                'form-3-mark': 'wrong',
                'question_text': 'question text',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MAX_NUM_FORMS': 4,
                'form-MIN_NUM_FORMS': 0,
                'continue': True,
            }
        )
        self.assertEqual(response_post.status_code, 302)
        # test success message
        messages = list(get_messages(response_post.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'SuccessFully Created Question and Choices. Create another for title')

    def test_both_forms_valid_and_no_finish_or_continue_button_click(self):
        ### create dummy post data ###
        response_post = self.client.post(
            reverse('dash:create-question-choice', args=[self.quiz.pk]),
            {
                'form-0-choice_text': 'choice0',
                'form-1-choice_text': 'choice1',
                'form-2-choice_text': 'choice2',
                'form-3-choice_text': 'choice3',
                'form-0-mark': 'wrong',
                'form-1-mark': 'wrong',
                'form-2-mark': 'wrong',
                'form-3-mark': 'wrong',
                'question_text': 'question text',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MAX_NUM_FORMS': 4,
                'form-MIN_NUM_FORMS': 0,
            }
        )
        self.assertEqual(response_post.status_code, 200)
        self.assertTemplateUsed(response_post, 'dashboard/create_quiz.html')
