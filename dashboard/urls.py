from django.urls import path, include
from django.contrib.auth import views as auth_views


from . import views

app_name = 'dash'

urlpatterns = [
    path('', views.DashView.as_view(), name='dashboard'),

    ### quiz url ###
    path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/<int:pk>/delete/',
         views.QuizDeleteView.as_view(), name='quiz-delete'),
    path('quiz/<int:pk>/update/',
         views.QuizUpdateView.as_view(), name='quiz-update'),

    ### question for quiz ###
    path('quiz/<int:pk>/questions/',
         views.QuizQuestionsListView.as_view(), name='quiz-questions'),

    ### question url ###
    path('questions/', views.QuestionListView.as_view(), name='question-list'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(),
         name='question-detail'),
    path('question/<int:pk>/delete/',
         views.QuestionDeleteView.as_view(), name='question-delete'),
    path('question/<int:pk>/update/',
         views.QuestionUpdateView.as_view(), name='question-update'),

    ### choice ###
    path('choice/<int:pk>/update/',
         views.ChoiceUpdateView.as_view(), name='choice-update'),

    # Create Quiz
    path('create-quiz/', views.CreateQuiz.as_view(), name='create-quiz'),
    path('quiz/<int:pk>/create-question-choice/',
         views.CreateQuestionAndChoice.as_view(), name='create-question-choice')

]


# REDUNDANT

#     path('quiz/create/', views.QuizCreateView.as_view(), name='quiz-create'),
#     path('question/', views.QuestionListView.as_view(), name='question-list'),
#     path('question/<int:pk>/', views.QuestionDetailView.as_view(),
#          name='question-detail'),
#     path('choice/<int:pk>/delete/',
#          views.ChoiceDeleteView.as_view(), name='choice-delete'),
#     path('question/create/', views.QuestionCreateView.as_view(),
#          name='question-create'),
#     path('quiz/<int:pk>/create-question/',
#          views.QuizQuestionCreateView.as_view(), name='quiz-question-create'),


### choices for question ###
#     path('question/<int:pk>/create-choice/',
#          views.QuestionChoiceCreateView.as_view(), name='question-choice-create'),
#     path('question/<int:pk>/choices/',
#          views.QuestionChoicesListView.as_view(), name='question-choices'),
