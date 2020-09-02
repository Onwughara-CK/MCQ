from django.urls import path, include
from django.contrib.auth import views as auth_views


from . import views

app_name = 'dash'

urlpatterns = [
    path('', views.DashView.as_view(), name='dashboard'),

    # story url
    path('story/', views.StoryListView.as_view(), name='story-list'),
    # path('story/<int:pk>/', views.StoryDetailView.as_view(), name='story-detail'),
    # path('story/<int:pk>/', views.StoryDeleteView.as_view(), name='story-delete'),
    # path('story/<int:pk>/update/',
    #      views.StoryUpdateView.as_view(), name='story-update'),
    # path('story/create/', views.StoryCreateView.as_view(), name='story-create'),
]
