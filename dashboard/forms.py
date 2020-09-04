from django import forms

from .models import Quiz, Question, Choice


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ['quiz_title', 'quiz_text', 'duration', ]


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text', ]

class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['mark', 'choice_text']
