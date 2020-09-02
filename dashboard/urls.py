from django.urls import path, include
from django.contrib.auth import views as auth_views


from . import views

app_name = 'dash'

urlpatterns = [
    path('', views.DashView.as_view(), name='dashboard'),
]
