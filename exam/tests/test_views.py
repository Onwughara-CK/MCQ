from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_duration
from django.contrib.messages import get_messages

from dashboard import models
from exam import models as exam_models


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
        self.response = self.client.get(reverse('exam:exam_list'))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('exam:exam_list'))
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
        cls.sample_quiz = models.Quiz.objects.create(
            quiz_title='sample', quiz_text='sample text')

    def setUp(self):
        self.client.login(
            email='teacher@test.com', password='asdf7890')
        self.response = self.client.get(
            reverse('exam:exam_instruction', args=[self.quiz.pk]))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_404_for_wrong_pk(self):
        response = self.client.get(
            reverse('exam:exam_instruction', args=[911]))
        self.assertEqual(response.status_code, 404)

    def test_sample_quiz(self):
        response = self.client.get(
            reverse('exam:sample_exam', args=['sample']))
        self.assertEqual(response.context['exam'],self.sample_quiz)
        

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
        """
        Responses for when a user types the exam questions url directly into the browser 
        without passing through the instructions page
        """
        self.response_no_instruct_page = self.client.get(
            reverse('exam:exam_questions_list', args=[self.quiz.pk]))
        
        self.client.get(
            reverse('exam:exam_instruction', args=[self.quiz.pk]))
        self.response_after_instruct_page = self.client.get(
            reverse('exam:exam_questions_list', args=[self.quiz.pk]))

    def test_access_exam_questions_without_passing_through_instructions_page(self):
        """ 
        When the instructions page of a quiz is loaded, a session variable of start-quiz
        is created and equated to True. If a user tries to access the exam questions
        without passing through the instruction page by typing the url of the exam
        directly into the browser, a Permission Denied is raised with status code 403        
        """
        self.assertEqual(self.response_no_instruct_page.status_code, 403)       

    def test_access_exam_questions_after_passing_through_instructions_page(self):        
        self.assertEqual(self.response_after_instruct_page.status_code, 200)

    def test_returns_correct_template(self):
        self.assertTemplateUsed(self.response_after_instruct_page, 'exam/exam_questions.html')

    def test_context_object(self):
        self.assertEqual(self.response_after_instruct_page.context['quiz_pk'], self.quiz.pk)
        self.assertIn('questions', self.response_after_instruct_page.context)

    def test_pagination(self):
        self.assertTrue(self.response_after_instruct_page.context['is_paginated'])
        self.assertEqual(
            self.response_after_instruct_page.context['paginator'].count, self.quiz.questions.count())
        self.assertEqual(self.response_after_instruct_page.context['paginator'].per_page, 1)


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
            quiz_title='title 1', 
            quiz_text='text 1',
            
        )

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
        self.response = self.client.get(reverse('exam:exam_result'))

    # test not login
    def test_guest_not_ajax(self):
        self.client.logout()
        response = self.client.get(reverse('exam:exam_result'))
        self.assertEqual(response.status_code, 404)
        # post
        response = self.client.post(reverse('exam:exam_result'))
        self.assertEqual(response.status_code, 404)

    def test_not_ajax(self):
        self.assertEqual(self.response.status_code, 404)
        # post
        response = self.client.post(reverse('exam:exam_result'))
        self.assertEqual(response.status_code, 404)

    def test_ajax_get(self):
        response = self.client.get(
            reverse('exam:exam_result'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        # receive json bytes, so decode byte to json and check
        self.assertJSONEqual(response.content.decode(), {})

    # test post as ajax without finish
    def test_ajax_post_not_finish(self):
        response = self.client.post(
            reverse('exam:exam_result'),
            data={},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {})

    def test_post_finish(self):
        response = self.client.post(
            reverse('exam:exam_result'),
            data={
                'finish': True,
                'quiz_pk': self.quiz.pk,
                'elapse':parse_duration('00:05:00'),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exam/result_sheet.html')
        self.assertEqual(response.context['no_of_questions'], 10)
        self.assertEqual(response.context['no_of_correct_choices_answered'], 0)
        self.assertEqual(response.context['no_of_questions_answered'], 0)
        self.assertEqual(response.context['percentage'], 0)

    def test_post_and_finish_with_correct_choices(self):
        response = self.client.post(
            reverse('exam:exam_result'),
            data={
                'finish': True,
                'elapse':parse_duration('00:05:00'),
                'quiz_pk': self.quiz.pk,
                'Question1': models.Choice.objects.filter(mark='right').first().pk,
                'Question2': models.Choice.objects.filter(mark='right').last().pk,
                'Question3': models.Choice.objects.filter(mark='wrong').last().pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exam/result_sheet.html')
        self.assertEqual(response.context['no_of_questions'], 10)
        self.assertEqual(response.context['no_of_correct_choices_answered'], 2)
        self.assertEqual(response.context['no_of_questions_answered'], 3)
        self.assertEqual(response.context['percentage'], 20)

    def test_post_and_get(self):
        data={                
                'Question1': 1,
                'Question2': 2,
        }
        self.client.post(
            reverse('exam:exam_result'),
            data,
        )

        response = self.client.get(reverse('exam:exam_result'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # receive json bytes, so decode byte to json and check
        self.assertJSONEqual(response.content.decode(), {                
                'Question1': '1',
                'Question2': '2',
        })

    def test_post_finish_not_authenticated(self):
        self.client.logout()
        response = self.client.post(
            reverse('exam:exam_result'),
            data={
                'finish': True,
                'quiz_pk': self.quiz.pk,
                'elapse':parse_duration('00:05:00'),
            },
        )
        self.assertTemplateUsed(response, 'exam/result_sheet.html')
        self.assertEqual(response.status_code, 200)
        


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
        response = self.client.post(reverse('exam:timer'))
        self.assertEqual(response.status_code, 404)

    def test_ajax_post_with_invalid_data(self):
        response = self.client.post(
            reverse('exam:timer'),
            data={},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 404)

    def test_ajax_post_with_valid_data(self):
        response = self.client.post(
            reverse('exam:timer'),
            data={
                'pk': self.quiz.pk,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)


class ExamResultListViewTest(TestCase):
    """
    Test Exam Result List View
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    ### create student ###
        cls.student = get_user_model().objects.create_user(
            email='student@test.com', password='asdf7890')

        cls.quiz = models.Quiz.objects.create(
            quiz_title='title 1', quiz_text='text 1', duration=timedelta(minutes=25))

        for i in range(1, 5):
            exam_models.Result.objects.create(
                percentage=i**2, 
                time_spent=timedelta(minutes=i*2),
                no_of_questions_answered = 2,
                no_of_correct_choices_answered = 4,
                no_of_questions = 6,
                user = cls.student,
                quiz = cls.quiz
            )

    def setUp(self):
        self.client.login(
            email='student@test.com', password='asdf7890')
        self.response = self.client.get(
            reverse('exam:result_list')
        )

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('exam:result_list'))
        self.assertRedirects(
            response, '/login/?next=/exam/resultList/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_correct_template(self):
        self.assertTemplateUsed(
            self.response, 'exam/result_list.html')

    def test_context_object(self):
        self.assertIn('results',self.response.context)
        self.assertCountEqual(
            self.response.context['results'], self.response.context['user'].results.all())




