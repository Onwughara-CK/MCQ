from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse

from exam import views


class UrlTest(SimpleTestCase):

    ### EXAM LIST VIEW ###
    def test_exam_list_url_resolves_to_exam_list_view(self):
        url = reverse('exam:exam-list')
        self.assertURLEqual(url, '/exam/')
        self.assertEqual(resolve(url).func.view_class,
                         views.ExamListView)

    ### EXAM INSTRUCTIONS VIEW ###
    def test_exam_instruction_url_resolves_to_exam_instruction_view(self):
        url = reverse('exam:exam-instruction', args=[1])
        self.assertURLEqual(url, '/exam/1/instructions/')
        self.assertEqual(resolve(url).func.view_class,
                         views.ExamInstructionsView)

    ### EXAM QUESTIONS LIST VIEW ###
    def test_exam_questions_list_url_resolves_to_view(self):
        url = reverse('exam:exam-questions-list', args=[1])
        self.assertURLEqual(url, '/exam/1/')
        self.assertEqual(resolve(url).func.view_class,
                         views.ExamQuestionsListView)

    ### EXAM RESULT VIEW ###
    def test_exam_result_url_resolves_to_exam_result_view(self):
        url = reverse('exam:exam-result')
        self.assertURLEqual(url, '/exam/result/')
        self.assertEqual(resolve(url).func.view_class,
                         views.ExamResultView)

    ### EXAM TIMER VIEW ###
    def test_exam_timer_url_resolves_to_exam_timer_view(self):
        url = reverse('exam:timer')
        self.assertURLEqual(url, '/exam/timer/')
        self.assertEqual(resolve(url).func.view_class,
                         views.ExamTimerView)
