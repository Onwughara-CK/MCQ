from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib import messages

from . import models


class DashView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/dash.html')

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class StoryListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = models.Story
    template_name = "dashboard/story_list.html"
    context_object_name = 'stories'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True
