from django.contrib import admin
from .models import Story, Question, Choice


class StoryAdmin(admin.ModelAdmin):
    list_display = ('story_title',)
    search_fields = ('story_title', 'story_text')
    ordering = ('story_title',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',)
    search_fields = ('question_text',)
    ordering = ('question_text',)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text',)
    search_fields = ('choice_text',)
    ordering = ('choice_text',)


admin.site.register(Story, StoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
