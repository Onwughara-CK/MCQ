from django.urls import path, include
from django.contrib.auth import views as auth_views


from . import views

app_name = 'users'

urlpatterns = [
    # home
    path('', views.IndexView.as_view(), name='home'),

    # login
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',
                                                redirect_authenticated_user=True,
                                                extra_context={
                                                    'title': 'Login'}
                                                ), name='login'),
    # logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # register
    path('register/', views.RegisterView.as_view(), name='register'),
]
