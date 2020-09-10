from django.urls import path

from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.ExamListView.as_view(),
         name='exam-list'),
    path('<int:pk>/', views.ExamQuestionsListView.as_view(),
         name='exam-questions-list'),
    path('result/', views.ExamResultView.as_view(),
         name='exam-result'),
]
