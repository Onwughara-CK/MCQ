from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from . import models
from . import forms


class DashView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/dash.html')

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuizListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = models.Quiz
    template_name = "dashboard/quiz_list.html"
    context_object_name = 'stories'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True

##### quiz #####


class QuizDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = models.Quiz
    template_name = "dashboard/quiz_detail.html"
    context_object_name = 'quiz'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuizDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.edit.DeleteView):
    model = models.Quiz
    success_url = reverse_lazy('dash:quiz-list')
    success_message = 'Successfully Deleted quiz'
    context_object_name = 'quiz'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class QuizUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    model = models.Quiz
    fields = '__all__'
    success_message = 'Successfully Updated quiz'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuizCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = models.Quiz
    fields = '__all__'
    success_message = 'Successfully created quiz'


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


### quiz QUESTION ###

class QuizQuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = models.Question
    fields = ('question_text',)
    success_message = 'Successfully created Question'

    def form_valid(self, form):
        form.instance.quiz = models.Quiz.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuizQuestionsListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "dashboard/quiz_question_list.html"
    context_object_name = 'questions'

    def get_queryset(self):
        return models.Quiz.objects.get(pk=self.kwargs['pk']).questions.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_title'] = models.Quiz.objects.get(
            pk=self.kwargs['pk']).quiz_title
        return context

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


### QUESTION CHOICES ###

class QuestionChoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = models.Choice
    fields = ('choice_text', 'mark',)
    success_message = 'Successfully created Choice'

    def form_valid(self, form):
        form.instance.question = models.Question.objects.get(
            pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dash:question-detail', args=[self.kwargs['pk']])

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuestionChoicesListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "dashboard/choice_list.html"
    context_object_name = 'choices'

    def get_queryset(self):
        return models.Question.objects.get(pk=self.kwargs['pk']).choices.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_text'] = models.Question.objects.get(
            pk=self.kwargs['pk']).question_text
        return context

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


# CHOICE
class ChoiceDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.edit.DeleteView):
    model = models.Choice
    # success_url = reverse_lazy('dash:question-choices', arg=[])
    success_message = 'Successfully Deleted Choice'
    context_object_name = 'choice'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True

    def get_success_url(self):
        question_pk = models.Choice.objects.get(
            pk=self.kwargs['pk']).question.pk
        return reverse('dash:question-choices', args=[question_pk])

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ChoiceUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    model = models.Choice
    fields = ('choice_text', 'mark',)
    success_message = 'Successfully Updated Choice'

    def get_success_url(self):
        question_pk = models.Choice.objects.get(
            pk=self.kwargs['pk']).question.pk
        return reverse('dash:question-choices', args=[question_pk])

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class CreateQuiz(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, generic.edit.FormView):
    def get(self, request):
        form = forms.QuizForm
        return render(request, 'dashboard/quiz_form.html', {'form': form})

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True
