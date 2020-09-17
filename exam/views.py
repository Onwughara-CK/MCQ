from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic, View
from django.http import JsonResponse, HttpResponse, Http404
from django.utils import timezone
from django.utils.dateparse import parse_duration

from dashboard.models import Quiz, Choice, Question


class ExamListView(LoginRequiredMixin, generic.ListView):
    model = Quiz
    template_name = "exam/exam_list.html"
    context_object_name = 'exams'


class ExamInstructionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        exam = get_object_or_404(Quiz, pk=kwargs['pk'])
        return render(request, 'exam/exam_instructions.html', {'exam': exam})


class ExamQuestionsListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'questions'
    template_name = 'exam/exam_questions.html'
    paginate_by = 1

    def get_queryset(self):
        queryset = Quiz.objects.get(
            pk=self.kwargs['pk']).questions.all().order_by('question_text')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_pk'] = self.kwargs['pk']
        return context


class ExamResultView(LoginRequiredMixin, View):
    def get(self, request):
        data = {}
        for k, v in request.session.items():
            if "Question" in k:
                data[k] = v
        if not request.is_ajax():
            raise Http404
        return JsonResponse(data)

    def post(self, request):
        for k, v in request.POST.items():
            request.session[k] = v
        if request.POST.get('finish'):
            if request.is_ajax():
                raise Http404
            correct_choices = Choice.objects.filter(
                question__quiz__pk=request.POST.get('quiz_pk')).filter(mark='right')
            result = {
                'no_of_questions': Quiz.objects.get(pk=request.POST.get('quiz_pk')).questions.count(),
                'no_of_correct_choices_answered': 0,
                'no_of_questions_answered': 0,
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
            for _, v in corrections.items():
                corrections_list.append(v)
            result['corrections'] = corrections_list
            result['score_percent'] = int(result['no_of_correct_choices_answered'] /
                                          result['no_of_questions'] * 100)
            for key in list(request.session.keys()):
                if not key.startswith('_'):
                    del request.session[key]
            return render(request, 'exam/result_sheet.html', result)
        return HttpResponse(status=204)


class ExamTimerView(View):
    timer = {}

    def get(self, request):
        if not request.is_ajax():
            raise Http404
        return HttpResponse(self.timer.get('deadline_in_ms'))

    def post(self, request):
        exam_duration = get_object_or_404(
            Quiz, pk=request.POST.get('pk')).duration
        delta = parse_duration(str(exam_duration))

        deadline = timezone.now() + delta
        self.timer['deadline_in_ms'] = int(deadline.timestamp()*1000)
        if not request.is_ajax():
            raise Http404
        return HttpResponse(self.timer.get('deadline_in_ms'))
