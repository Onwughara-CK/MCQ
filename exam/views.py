from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic, View

from dashboard.models import Quiz, Choice, Question


class ExamListView(LoginRequiredMixin, generic.ListView):
    model = Quiz
    template_name = "exam/exam_list.html"
    context_object_name = 'exams'


class ExamQuestionsListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'questions'
    template_name = 'exam/exam_questions.html'
    paginate_by = 1

    def get_queryset(self):
        queryset = Quiz.objects.get(pk=self.kwargs['pk']).questions.all()
        return queryset
