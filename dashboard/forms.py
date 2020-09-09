from django import forms

from .models import Quiz, Question, Choice


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['duration', 'quiz_title', 'quiz_text', ]


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text', ]


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['choice_text', 'mark']
