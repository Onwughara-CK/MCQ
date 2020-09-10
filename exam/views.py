from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic, View
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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
        queryset = Quiz.objects.get(
            pk=self.kwargs['pk']).questions.all().order_by('question_text')
        return queryset


@method_decorator(csrf_exempt, name='post')
class ExamResultView(LoginRequiredMixin, View):
    def get(self, request):
        data = {}
        for k, v in request.session.items():
            if "Question" in k:
                data[k] = v
        return JsonResponse(data)

    def post(self, request):
        for k, v in request.POST.items():
            request.session[k] = v
        return HttpResponse('works')
