from django import forms
from django.forms import BaseFormSet

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

class BaseChoiceFormSet(BaseFormSet):
    def __init__(self,*args,**kwargs):        
        super().__init__(*args,**kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        """Checks that no two choices have the same text."""
        if any(self.errors):#Don't bother if any form has an error
            return
        choices_text = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            choice_text = form.cleaned_data.get('choice_text').lower()
            if choice_text in choices_text:
                raise forms.ValidationError("choices in a question set must have distinct text.")
            choices_text.append(choice_text)
