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


class StoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Story
    template_name = "dashboard/story_detail.html"
    context_object_name = 'story'


class StoryDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.edit.DeleteView):
    model = models.Story
    success_url = reverse_lazy('dash:story-list')
    success_message = 'Successfully Deleted Story'
    context_object_name = 'story'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class StoryUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    model = models.Story
    fields = '__all__'
    success_message = 'Successfully Updated Story'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class StoryCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = models.Story
    fields = '__all__'
    success_message = 'Successfully created Story'
