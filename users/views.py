from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from django.views import View

from .forms import RegisterForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/index.html')


class RegisterView(FormView):
    def get(self, request):
        form = RegisterForm
        context = {
            'form': form,
            'title': 'Register'
        }
        return render(request, 'users/gate.html', context)

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect(reverse('users:home'))
        return render(request, 'users/gate.html', {'form': form})
