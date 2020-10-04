from django.test import SimpleTestCase
from django.urls import resolve, reverse


from dashboard import views


class UrlTest(SimpleTestCase):

    ### DASH VIEW ###

    def test_dashboard_url_resolves_to_dash_view(self):
        url = reverse('dash:dashboard')
        self.assertURLEqual(url, '/dashboard/')
        self.assertEqual(resolve(url).func.view_class,
                         views.DashView)

    def test_dashboard_url_fails_resolve_to_Quiz_list_view(self):
        url = reverse('dash:dashboard')
        self.assertNotEqual(url, '/dashboard/quizzes/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.QuizListView)

    ### QUIZ LIST VIEW ###

    def test_quiz_list_url_resolves_to_quiz_list_view(self):
        url = reverse('dash:quiz_list')
        self.assertURLEqual(url, '/dashboard/quizzes/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuizListView)

    def test_quiz_list_url_fails_resolve_to__list_view(self):
        url = reverse('dash:quiz_list')
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### QUIZ DETAIL VIEW ###

    def test_quiz_detail_url_resolves_to_quiz_detail_view(self):
        url = reverse('dash:quiz_detail', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/quiz/{1}/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuizDetailView)

    def test_quiz_detail_url_fails_resolve_to__detail_view(self):
        url = reverse('dash:quiz_detail', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### QUIZ DELETE VIEW ###

    def test_quiz_delete_url_resolves_to_quiz_delete_view(self):
        url = reverse('dash:quiz_delete', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/quiz/{1}/delete/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuizDeleteView)

    def test_quiz_delete_url_fails_resolve_to_delete_view(self):
        url = reverse('dash:quiz_delete', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### QUIZ UPDATE VIEW ###

    def test_quiz_update_url_resolves_to_quiz_update_view(self):
        url = reverse('dash:quiz_update', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/quiz/{1}/update/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuizUpdateView)

    def test_quiz_update_url_fails_resolve_to_update_view(self):
        url = reverse('dash:quiz_update', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### QUZ QUESTIONS LIST VIEW ###

    def test_quiz_questions_list_view_url_resolves_to_quiz_questions_list_view(self):
        url = reverse(
            'dash:quiz_questions', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/quiz/{1}/questions/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuizQuestionsListView)

    def test_quiz_questions_list_url_fails_resolve_to_quiz_questions_list_view(self):
        url = reverse(
            'dash:quiz_questions', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### QUESTIONS LIST VIEW ###

    def test_questions_list_view_url_resolves_to_questions_list_view(self):
        url = reverse('dash:question_list')
        self.assertURLEqual(
            url, f'/dashboard/questions/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuestionListView)

    def test_questions_list_url_fails_resolve_to_questions_list_view(self):
        url = reverse('dash:question_list')
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### QUESTION DETAIL VIEW ###

    def test_question_detail_url_resolves_to_question_detail_view(self):
        url = reverse('dash:question_detail', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/question/{1}/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuestionDetailView)

    def test_question_detail_url_fails_resolve_to_question_detail_view(self):
        url = reverse('dash:question_detail', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### QUESTION DELETE VIEW ###

    def test_question_delete_url_resolves_to_question_delete_view(self):
        url = reverse('dash:question_delete', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/question/{1}/delete/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuestionDeleteView)

    def test_question_delete_url_fails_resolve_to_question_delete_view(self):
        url = reverse('dash:question_delete', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### QUESTION UPDATE VIEW ###

    def test_question_update_url_resolves_to_question_update_view(self):
        url = reverse('dash:question_update', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/question/{1}/update/')
        self.assertEqual(resolve(url).func.view_class,
                         views.QuestionUpdateView)

    def test_question_update_url_fails_resolve_to_question_update_view(self):
        url = reverse('dash:question_update', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### CHOICE UPDATE VIEW ###

    def test_choice_update_url_resolves_to_choice_update_view(self):
        url = reverse('dash:choice_update', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/choice/{1}/update/')
        self.assertEqual(resolve(url).func.view_class,
                         views.ChoiceUpdateView)

    def test_choice_update_url_fails_resolve_to_choice_update_view(self):
        url = reverse('dash:choice_update', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### CREATE QUIZ VIEW ###
    def test_create_quiz_url_resolves_to_create_quiz_view(self):
        url = reverse('dash:create_quiz')
        self.assertURLEqual(
            url, f'/dashboard/create_quiz/')
        self.assertEqual(resolve(url).func.view_class,
                         views.CreateQuiz)

    def test_create_quiz_url_fails_resolve_to_create_quiz_view(self):
        url = reverse('dash:create_quiz')
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)

    ### CREATE QUESTION AND CHOICE VIEW ###

    def test_create_question_and_choice_url_resolves_to_create_question_and_choice_view(self):
        url = reverse('dash:create_question_choice', args=[1])
        self.assertURLEqual(
            url, f'/dashboard/quiz/{1}/create_question_choice/')
        self.assertEqual(resolve(url).func.view_class,
                         views.CreateQuestionAndChoice)

    def test_create_question_and_choice_url_fails_resolve_to_create_question_and_choice_view(self):
        url = reverse('dash:create_question_choice', args=[1])
        self.assertNotEqual(url, '/dashboard/')
        self.assertNotEqual(resolve(url).func.view_class,
                            views.DashView)
