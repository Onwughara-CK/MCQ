from django.urls import resolve, reverse
from django.test import SimpleTestCase, TestCase

from users import views as users_views
from dashboard import views as dash_views
from exam import views as exam_views



class UrlTest(TestCase):
    def test_home_url(self):
        self.assertEqual(resolve('/').func.view_class,users_views.IndexView)
        self.assertEqual(resolve('/').namespace,'users')

    def test_dashboard_url(self):
        self.assertEqual(resolve('/dashboard/').func.view_class,dash_views.DashView)
        self.assertEqual(resolve('/dashboard/').namespace,'dash')

    def test_exam_url(self):
        self.assertEqual(resolve('/exam/').func.view_class,exam_views.ExamListView)
        self.assertEqual(resolve('/exam/').namespace,'exam')




