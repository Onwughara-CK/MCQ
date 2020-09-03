from django.urls import path, include
from django.contrib.auth import views as auth_views


from . import views

app_name = 'dash'

urlpatterns = [
    path('', views.DashView.as_view(), name='dashboard'),

    # story url
    path('story/', views.StoryListView.as_view(), name='story-list'),
    path('story/<int:pk>/', views.StoryDetailView.as_view(), name='story-detail'),
    path('story/<int:pk>/delete/',
         views.StoryDeleteView.as_view(), name='story-delete'),
    path('story/<int:pk>/update/',
         views.StoryUpdateView.as_view(), name='story-update'),
    path('story/create/', views.StoryCreateView.as_view(), name='story-create'),


    # question url
    path('question/', views.QuestionListView.as_view(), name='question-list'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(),
         name='question-detail'),
    path('question/<int:pk>/delete/',
         views.QuestionDeleteView.as_view(), name='question-delete'),
    path('question/<int:pk>/update/',
         views.StoryUpdateView.as_view(), name='question-update'),
    #     path('story/create/', views.StoryCreateView.as_view(), name='story-create'),
]
