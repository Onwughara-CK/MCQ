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

##### STORY #####


class StoryDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = models.Story
    template_name = "dashboard/story_detail.html"
    context_object_name = 'story'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


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


###### QUESTION ######

class QuestionListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = models.Question
    template_name = "dashboard/question_list.html"
    context_object_name = 'questions'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuestionDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Question
    template_name = "dashboard/question_detail.html"
    context_object_name = 'question'


class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.edit.DeleteView):
    model = models.Question
    success_url = reverse_lazy('dash:question-list')
    success_message = 'Successfully Deleted Question'
    context_object_name = 'question'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    model = models.Question
    fields = '__all__'
    success_message = 'Successfully Updated Question'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuestionCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = models.Question
    fields = '__all__'
    success_message = 'Successfully created Question'


### STORY QUESTION ###

class StoryQuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = models.Question
    fields = ('question_text',)
    success_message = 'Successfully created Question'

    def form_valid(self, form):
        form.instance.story = models.Story.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class StoryQuestionsListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "dashboard/question_list.html"
    context_object_name = 'questions'

    def get_queryset(self):
        return models.Story.objects.get(pk=self.kwargs['pk']).questions.all()

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True
