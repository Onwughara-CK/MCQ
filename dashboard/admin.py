from django.contrib import admin
from .models import Quiz, Question, Choice


class QuizAdmin(admin.ModelAdmin):
    list_display = ('quiz_title',)
    search_fields = ('quiz_title', 'quiz_text')
    ordering = ('quiz_title',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',)
    search_fields = ('question_text',)
    ordering = ('question_text',)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text',)
    search_fields = ('choice_text',)
    ordering = ('choice_text',)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
