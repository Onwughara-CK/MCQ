from django.urls import path

from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.ExamListView.as_view(),
         name='exam_list'),
    path('<int:pk>/instructions/', views.ExamInstructionsView.as_view(),
         name='exam_instruction'),
    path('<str:sample>/instructions/', views.ExamInstructionsView.as_view(),
         name='sample_exam'),
    path('<int:pk>/', views.ExamQuestionsListView.as_view(),
         name='exam_questions_list'),
    path('result/', views.ExamResultView.as_view(),
         name='exam_result'),
    path('timer/', views.ExamTimerView.as_view(),
         name='timer'),
]
