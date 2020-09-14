from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse
from django.forms import formset_factory


from .models import Quiz, Choice, Question
from .forms import QuizForm, QuestionForm, ChoiceForm


class DashView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/dash.html')

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuizListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Quiz
    template_name = "dashboard/quiz_list.html"
    context_object_name = 'quizzes'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True

##### quiz #####


class QuizDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Quiz
    template_name = "dashboard/quiz_detail.html"
    context_object_name = 'quiz'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuizDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.edit.DeleteView
):
    model = Quiz
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


class QuizUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    generic.edit.UpdateView
):
    model = Quiz
    fields = ('quiz_text', 'duration', 'quiz_title')
    success_message = 'Successfully Updated quiz'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


###### QUESTION ######

class QuestionListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Question
    template_name = "dashboard/question_list.html"
    context_object_name = 'questions'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuestionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "dashboard/question_detail.html"
    context_object_name = 'question'


class QuestionDeleteView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    generic.edit.DeleteView
):
    model = Question
    success_message = 'Successfully Deleted Question'
    context_object_name = 'question'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True

    def get_success_url(self):
        return reverse('dash:quiz-questions', args=[self.object.quiz.pk])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class QuestionUpdateView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.edit.UpdateView
):
    model = Question
    fields = ('question_text',)
    success_message = 'Successfully Updated Question'

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class QuizQuestionsListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.ListView
):
    template_name = "dashboard/quiz_question_list.html"
    context_object_name = 'questions'

    def get_queryset(self):
        return Quiz.objects.get(pk=self.kwargs['pk']).questions.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_title'] = Quiz.objects.get(
            pk=self.kwargs['pk']).quiz_title
        return context

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class ChoiceUpdateView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.edit.UpdateView
):
    model = Choice
    fields = ('choice_text', 'mark',)
    success_message = 'Successfully Updated Choice'

    def get_success_url(self):
        question_pk = Choice.objects.get(
            pk=self.kwargs['pk']).question.pk
        return reverse('dash:question-detail', args=[question_pk])

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class CreateQuiz(
    UserPassesTestMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.edit.FormView
):
    def get(self, request):

        context = {
            'form': QuizForm(),
        }

        return render(request, 'dashboard/create_quiz.html', context)

    def post(self, request):
        quizForm = QuizForm(request.POST)

        if quizForm.is_valid():
            qf = quizForm.save(commit=False)
            qf.save()

            if request.POST.get('finish', None):
                return redirect(reverse('dash:quiz-list'), permanent=True)
            if request.POST.get('continue', None):
                return HttpResponse(qf.pk)
                # return redirect(reverse('dash:create-question-answer'), permanent=True)
        return render(request, 'dashboard/create_quiz.html', {'form': quizForm})

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True


class CreateQuestionAndChoice(
    UserPassesTestMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.edit.FormView
):

    ChoiceFormSet = formset_factory(ChoiceForm, extra=4, max_num=4)

    def get(self, request, *args, **kwargs):

        context = {
            'QuestionForm': QuestionForm(),
            'ChoiceForm': self.ChoiceFormSet(),
        }

        return render(request, 'dashboard/create_quiz.html',  context)

    def post(self, request, *args, **kwargs):

        questForm = QuestionForm(request.POST)
        formset = self.ChoiceFormSet(request.POST)

        context = {
            'QuestionForm': questForm,
            'ChoiceForm': formset,
        }

        if questForm.is_valid() and formset.is_valid():
            qf = questForm.save(commit=False)
            qz = Quiz.objects.get(pk=kwargs['pk'])
            qf.quiz = qz
            qf.save()
            for form in formset:
                instance = form.save(commit=False)
                instance.question = qf
                instance.save()
            if request.POST.get('finish', None):
                return redirect(reverse('dash:quiz-list'), permanent=True)
            if request.POST.get('continue', None):
                return HttpResponse(qz.pk)
        return render(request, 'dashboard/create_quiz.html', context)

    def test_func(self):
        user = self.request.user
        if not user.teacher:
            raise PermissionDenied
        return True
