from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic, View
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotFound
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.utils.dateparse import parse_duration

from dashboard.models import Quiz, Choice, Question
from .models import Result


def clearSessionWithoutLoggingOut(request):
    """clears session without logging user out"""
    for key in list(request.session.keys()):
        if not key.startswith('_'):
            del request.session[key]
    return

class ExamListView(LoginRequiredMixin, generic.ListView):
    model = Quiz
    template_name = "exam/exam_list.html"
    context_object_name = 'exams'

    def get(self, request, *args, **kwargs):
        clearSessionWithoutLoggingOut(request)
        return super().get(request, *args, **kwargs)


class ExamInstructionsView(View):
    def get(self, request, *args, **kwargs):
        clearSessionWithoutLoggingOut(request)
        request.session['start-quiz'] = True
        if kwargs.get('sample'):
            exam = get_object_or_404(Quiz, quiz_title='sample')            
        else:
            exam = get_object_or_404(Quiz, pk=kwargs['pk'])
        return render(request, 'exam/exam_instructions.html', {'exam': exam})


class ExamQuestionsListView(UserPassesTestMixin, generic.ListView):
    context_object_name = 'questions'
    template_name = 'exam/exam_questions.html'
    paginate_by = 1

    def test_func(self):
        if self.request.session.get('start-quiz') != True:
            clearSessionWithoutLoggingOut(self.request)
            raise PermissionDenied
        return True

    def get_queryset(self):
        queryset = Quiz.objects.get(
            pk=self.kwargs['pk']).questions.all().order_by('question_text')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_pk'] = self.kwargs['pk']
        return context

class ExamResultView(View):
    def get(self, request):
        data = {}
        for key, value in request.session.items():
            if "Question" in key:
                data[key] = value
        if not request.is_ajax():
            raise Http404
        return JsonResponse(data)

    def post(self, request):
        for key, value in request.POST.items():
            request.session[key] = value
        if not request.POST.get('finish'):
            return self.get(request)
        correct_choices = Choice.objects.filter(
            question__quiz__pk=request.POST.get('quiz_pk')).filter(mark='right')
        result = {
            'no_of_questions': Quiz.objects.get(pk=request.POST.get('quiz_pk')).questions.count(),
            'no_of_correct_choices_answered': 0,
            'no_of_questions_answered': 0,
            'pk':request.POST.get('quiz_pk'),
        }
        corrections = {}
        corrections_list = []
        for correct_choice in correct_choices:
            corrections[correct_choice.question.pk] = {
                'question': correct_choice.question.question_text,
                'correct_choice': correct_choice.choice_text,
                'your_choice': 'You Did not Answer This Question',
            }
        for question_id, your_choice_id in request.session.items():
            if 'Question' in question_id:
                result['no_of_questions_answered'] += 1
                your_choice = Choice.objects.get(
                    pk=your_choice_id)
                corrections[your_choice.question.pk]['your_choice'] = your_choice.choice_text
                if your_choice in correct_choices:
                    result['no_of_correct_choices_answered'] += 1
        for _, value in corrections.items():
            corrections_list.append(value)
        result['corrections'] = corrections_list
        result['percentage'] = int(result['no_of_correct_choices_answered'] /
                                        result['no_of_questions'] * 100)
        result['time_spent'] = request.POST.get('elapse')
        clearSessionWithoutLoggingOut(request)
        if request.user.is_authenticated:
            Result.objects.create(
                percentage= result['percentage'],
                user = request.user,
                time_spent = parse_duration(result['time_spent']),
                no_of_questions_answered = result['no_of_questions_answered'],
                no_of_correct_choices_answered = result['no_of_correct_choices_answered'],
                no_of_questions = result['no_of_questions'],
                quiz = Quiz.objects.get(pk=request.POST.get('quiz_pk')),
            )
        return render(request, 'exam/result_sheet.html', result)
        
class ExamTimerView(View):
    def post(self, request):
        if not request.is_ajax():
            raise Http404
        exam_duration = get_object_or_404(
            Quiz, pk=request.POST.get('pk')).duration
        return HttpResponse(str(exam_duration))

class ExamResultListView(LoginRequiredMixin, generic.ListView):
    template_name = 'exam/result_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = self.request.user.results.all().order_by('-date')
        return queryset

